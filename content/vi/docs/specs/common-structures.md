---
title: "Cấu trúc chung"
description: "Các kiểu dữ liệu dùng chung và các định dạng tuần tự hóa được sử dụng xuyên suốt các đặc tả I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Tổng quan

Tài liệu này đặc tả các cấu trúc dữ liệu cơ bản được sử dụng trong toàn bộ các giao thức I2P, bao gồm [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) và những giao thức khác. Các cấu trúc dùng chung này đảm bảo khả năng tương tác giữa các bản triển khai I2P khác nhau và các lớp giao thức.

### Những thay đổi chính kể từ 0.9.58

- ElGamal và DSA-SHA1 không còn được khuyến nghị cho Router Identities (sử dụng X25519 + EdDSA)
- Hỗ trợ ML-KEM hậu lượng tử đang trong giai đoạn thử nghiệm beta (tùy chọn tham gia (opt-in) kể từ 2.10.0)
- Các tùy chọn bản ghi dịch vụ đã được chuẩn hóa ([Proposal 167](/proposals/167-service-records/), được triển khai trong 0.9.66)
- Đặc tả đệm có thể nén đã được hoàn tất ([Proposal 161](/vi/proposals/161-ri-dest-padding/), được triển khai trong 0.9.57)

---

## Đặc tả kiểu dữ liệu dùng chung

### Số nguyên

**Mô tả:** Đại diện cho một số nguyên không âm theo thứ tự byte mạng (big-endian: byte có trọng số cao ở trước).

**Nội dung:** 1 đến 8 byte biểu diễn một số nguyên không dấu.

**Cách dùng:** Độ dài trường, số lượng, định danh kiểu, và các giá trị số trong toàn bộ các giao thức I2P.

---

### Ngày

**Mô tả:** Dấu thời gian biểu thị số mili giây kể từ kỷ nguyên Unix (ngày 1 tháng 1 năm 1970 00:00:00 GMT).

**Nội dung:** Số nguyên 8 byte (unsigned long, số nguyên không dấu kiểu long)

**Giá trị đặc biệt:** - `0` = Ngày không xác định hoặc null - Giá trị tối đa: `0xFFFFFFFFFFFFFFFF` (năm 584,942,417,355)

**Lưu ý triển khai:** - Luôn dùng múi giờ UTC/GMT - Yêu cầu độ chính xác đến mili giây - Được dùng cho việc hết hạn lease (bản ghi thuê trong I2P), công bố RouterInfo, và kiểm tra hợp lệ dấu thời gian

---

### Chuỗi

**Mô tả:** Chuỗi được mã hóa UTF-8 có tiền tố độ dài.

**Định dạng:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Ràng buộc:** - Độ dài tối đa: 255 byte (không phải số ký tự - các chuỗi UTF-8 nhiều byte được tính là nhiều byte) - Độ dài có thể bằng 0 (chuỗi rỗng) - Null terminator (ký tự kết thúc chuỗi null) KHÔNG được bao gồm - Chuỗi KHÔNG được kết thúc bằng null

**Quan trọng:** Các chuỗi UTF-8 có thể sử dụng nhiều byte cho mỗi ký tự. Một chuỗi có 100 ký tự có thể vượt quá giới hạn 255 byte nếu sử dụng ký tự đa byte.

---

## Cấu trúc khóa mật mã

### Khóa công khai

**Description:** Khóa công khai dùng cho mã hóa bất đối xứng. Loại khóa và độ dài phụ thuộc vào ngữ cảnh hoặc được chỉ định trong một Key Certificate (chứng thư khóa).

**Loại mặc định:** ElGamal (không còn được khuyến nghị cho Định danh router kể từ 0.9.58)

**Các kiểu được hỗ trợ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Yêu cầu triển khai:**

1. **X25519 (Type 4) - Tiêu chuẩn hiện hành:**
   - Được sử dụng cho cơ chế mã hóa ECIES-X25519-AEAD-Ratchet
   - Bắt buộc đối với Danh tính Router kể từ 0.9.48
   - Mã hóa kiểu little-endian (thứ tự byte nhỏ trước) (không giống các kiểu khác)
   - Xem [ECIES](/docs/specs/ecies/) và [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - Cũ (legacy):**
   - Không còn được khuyến nghị dùng cho Danh tính Router kể từ 0.9.58
   - Vẫn hợp lệ cho Đích (Destination) (trường này không được sử dụng từ 0.6/2005)
   - Sử dụng các số nguyên tố hằng được định nghĩa trong [ElGamal specification](/docs/specs/cryptography/)
   - Hỗ trợ được duy trì nhằm tương thích ngược

3. **MLKEM (Hậu lượng tử) - Beta:**
   - Cách tiếp cận lai kết hợp ML-KEM với X25519
   - KHÔNG được bật theo mặc định trong 2.10.0
   - Yêu cầu kích hoạt thủ công thông qua Hidden Service Manager
   - Xem [ECIES-HYBRID](/docs/specs/ecies/#hybrid) và [Đề xuất 169](/proposals/169-pq-crypto/)
   - Mã loại và đặc tả có thể thay đổi

**Tài liệu JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Khóa riêng

**Mô tả:** Khóa riêng cho giải mã bất đối xứng, tương ứng với các kiểu PublicKey.

**Lưu trữ:** Kiểu và độ dài được suy ra từ ngữ cảnh hoặc được lưu trữ riêng trong các cấu trúc dữ liệu/tệp khóa.

**Các kiểu được hỗ trợ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Ghi chú bảo mật:** - Các khóa riêng PHẢI được tạo bằng bộ sinh số ngẫu nhiên an toàn cho mật mã - Các khóa riêng X25519 sử dụng scalar clamping (ép ngưỡng vô hướng) như được định nghĩa trong RFC 7748 - Dữ liệu khóa PHẢI được xóa an toàn khỏi bộ nhớ khi không còn cần thiết

**JavaDoc (tài liệu API Java):** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Khóa phiên

**Mô tả:** Khóa đối xứng dùng cho mã hóa và giải mã AES-256 trong tunnel và garlic encryption của I2P.

**Nội dung:** 32 byte (256 bit)

**Sử dụng:** - Mã hóa lớp tunnel (AES-256/CBC with IV) - Mã hóa thông điệp bằng garlic encryption (cơ chế mã hóa đặc trưng của I2P) - Mã hóa phiên đầu-cuối

**Sinh:** PHẢI sử dụng bộ sinh số ngẫu nhiên an toàn mật mã.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Mô tả:** Khóa công khai dùng để xác minh chữ ký. Kiểu và độ dài được xác định trong Key Certificate (chứng chỉ khóa) của Destination (đích) hoặc được suy ra từ ngữ cảnh.

**Kiểu mặc định:** DSA_SHA1 (đã lỗi thời kể từ 0.9.58)

**Các loại được hỗ trợ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Yêu cầu triển khai:**

1. **EdDSA_SHA512_Ed25519 (Loại 7) - Tiêu chuẩn hiện tại:**
   - Mặc định cho tất cả các định danh router và điểm đích mới kể từ cuối năm 2015
   - Sử dụng đường cong Ed25519 với băm SHA-512
   - Khóa công khai 32 byte, chữ ký 64 byte
   - Mã hóa theo thứ tự little-endian (khác với đa số các loại khác)
   - Hiệu năng và bảo mật cao

2. **RedDSA_SHA512_Ed25519 (Type 11) - Chuyên biệt:**
   - CHỈ dùng cho các leasesets được mã hóa và blinding (kỹ thuật làm mù)
   - Không bao giờ dùng cho Router Identities hoặc Destinations chuẩn
   - Các khác biệt chính so với EdDSA:
     - Khóa riêng bằng phép giảm modulo (không dùng clamping (thiết lập một số bit cố định))
     - Chữ ký bao gồm 80 byte dữ liệu ngẫu nhiên
     - Sử dụng trực tiếp khóa công khai (không dùng giá trị băm của khóa riêng)
   - Xem [Đặc tả Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - Cũ:**
   - Không còn được khuyến nghị (deprecated) cho Router Identities (danh tính router) kể từ 0.9.58
   - Không khuyến khích dùng cho các Destinations (điểm đích trong I2P) mới
   - DSA 1024-bit với SHA-1 (đã biết có điểm yếu)
   - Chỉ duy trì hỗ trợ vì mục đích tương thích

4. **Khóa gồm nhiều phần tử:**
   - Khi được cấu thành từ hai phần tử (ví dụ: các điểm ECDSA (thuật toán chữ ký số đường cong elliptic) X,Y)
   - Mỗi phần tử được đệm thêm số 0 ở đầu để đạt độ dài bằng một nửa
   - Ví dụ: khóa ECDSA 64 byte = 32 byte X + 32 byte Y

**Tài liệu JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Mô tả:** Khóa riêng dùng để tạo chữ ký, tương ứng với các kiểu SigningPublicKey (khóa công khai dùng để ký).

**Lưu trữ:** Kiểu và độ dài được chỉ định khi tạo.

**Các loại được hỗ trợ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Yêu cầu bảo mật:** - Sinh bằng nguồn sinh số ngẫu nhiên an toàn về mật mã - Bảo vệ bằng các cơ chế kiểm soát truy cập phù hợp - Xóa khỏi bộ nhớ một cách an toàn khi hoàn tất - Với EdDSA: seed 32 byte được băm bằng SHA-512, 32 byte đầu trở thành giá trị vô hướng (clamp: chỉnh các bit theo quy tắc) - Với RedDSA: Cách sinh khóa khác (giảm modulo thay vì clamp)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Chữ ký

**Mô tả:** Chữ ký mật mã trên dữ liệu, sử dụng thuật toán ký tương ứng với kiểu SigningPrivateKey.

**Loại và độ dài:** Suy ra từ loại khóa được dùng để ký.

**Các loại được hỗ trợ:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Ghi chú về định dạng:** - Chữ ký nhiều thành phần (ví dụ, các giá trị R,S của ECDSA) được đệm bằng số 0 ở đầu để mỗi thành phần có độ dài bằng length/2 - EdDSA và RedDSA sử dụng mã hóa theo thứ tự byte little-endian (thứ tự byte thấp trước) - Tất cả các loại khác sử dụng mã hóa theo thứ tự byte big-endian

**Xác minh:** - Sử dụng SigningPublicKey (khóa công khai dùng để ký) tương ứng - Tuân theo các đặc tả của thuật toán chữ ký số cho loại khóa - Kiểm tra rằng độ dài chữ ký khớp với độ dài dự kiến cho loại khóa

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Mã băm

**Mô tả:** Giá trị băm SHA-256 của dữ liệu, được sử dụng xuyên suốt I2P để xác minh tính toàn vẹn và nhận diện.

**Nội dung:** 32 byte (256 bit)

**Mục đích sử dụng:** - Băm định danh Router (khóa cơ sở dữ liệu mạng) - Băm Destination (đích trong I2P) (khóa cơ sở dữ liệu mạng) - Định danh cổng vào của Tunnel trong Leases (bản ghi Lease trong I2P) - Xác minh tính toàn vẹn dữ liệu - Sinh ID Tunnel

**Thuật toán:** SHA-256 như được định nghĩa trong FIPS 180-4

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Session Tag (thẻ phiên)

**Mô tả:** Số ngẫu nhiên được dùng để định danh phiên và mã hóa dựa trên thẻ.

**Quan trọng:** Kích thước Session Tag (thẻ phiên) thay đổi theo kiểu mã hóa: - **ElGamal/AES+SessionTag:** 32 byte (cũ) - **ECIES-X25519:** 8 byte (tiêu chuẩn hiện tại)

**Tiêu chuẩn hiện hành (ECIES):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Xem [ECIES](/docs/specs/ecies/) và [ECIES-ROUTERS](/docs/specs/ecies/#routers) để xem các đặc tả chi tiết.

**Kiểu cũ (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Sinh:** PHẢI sử dụng bộ sinh số ngẫu nhiên an toàn mật mã.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Mô tả:** Mã định danh duy nhất cho vị trí của router trong một tunnel. Mỗi chặng trong một tunnel có một TunnelId (mã định danh của tunnel) riêng.

**Định dạng:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Sử dụng:** - Xác định các kết nối tunnel vào/ra tại mỗi router - TunnelId khác nhau tại mỗi hop (chặng) trong chuỗi tunnel - Được dùng trong các cấu trúc Lease để xác định các tunnel gateway

**Các giá trị đặc biệt:** - `0` = Dành riêng cho các mục đích đặc thù của giao thức (tránh sử dụng trong hoạt động bình thường) - TunnelIds (định danh tunnel) chỉ có ý nghĩa cục bộ trên từng router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Đặc tả Chứng chỉ

### Chứng chỉ

**Mô tả:** Bộ chứa dùng cho các biên nhận, bằng chứng công việc (proof-of-work), hoặc siêu dữ liệu mật mã được sử dụng xuyên suốt I2P.

**Định dạng:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Tổng kích thước:** tối thiểu 3 byte (NULL certificate), tối đa 65538 byte

### Các loại chứng chỉ

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Chứng chỉ khóa (Loại 5)

**Giới thiệu:** Phiên bản 0.9.12 (Tháng 12 năm 2013)

**Mục đích:** Chỉ định các kiểu khóa không mặc định và lưu trữ dữ liệu khóa dư thừa vượt quá cấu trúc KeysAndCert tiêu chuẩn 384 byte.

**Cấu trúc tải trọng dữ liệu:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Các lưu ý triển khai quan trọng:**

1. **Thứ tự kiểu khóa:**
   - **CẢNH BÁO:** Kiểu khóa ký đứng TRƯỚC kiểu khóa mật mã
   - Điều này có vẻ ngược trực giác nhưng được duy trì để đảm bảo tương thích
   - Thứ tự: SPKtype, CPKtype (không phải CPKtype, SPKtype)

2. **Bố cục dữ liệu khóa trong KeysAndCert (khóa và chứng chỉ):**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Tính toán dữ liệu khóa dư thừa:**
   - Nếu Crypto Key > 256 byte: Excess = (Crypto Length - 256)
   - Nếu Signing Key > 128 byte: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Ví dụ (Khóa mật mã ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Yêu cầu về danh tính Router:** - Chứng chỉ NULL được sử dụng cho đến phiên bản 0.9.15 - Key Certificate (chứng chỉ khóa) được yêu cầu cho các loại khóa không mặc định kể từ phiên bản 0.9.16 - Các khóa mã hóa X25519 được hỗ trợ kể từ phiên bản 0.9.48

**Yêu cầu đối với Điểm đích:** - chứng chỉ NULL hoặc Key Certificate (chứng chỉ khóa, khi cần) - Key Certificate bắt buộc cho các loại khóa ký không mặc định từ 0.9.12 - Trường khóa công khai mật mã không còn được dùng từ 0.6 (2005) nhưng vẫn phải có

**Cảnh báo quan trọng:**

1. **Chứng chỉ NULL vs KEY:**
   - Chứng chỉ KEY với kiểu (0,0) chỉ định ElGamal+DSA_SHA1 được phép nhưng không khuyến khích
   - Luôn dùng chứng chỉ NULL cho ElGamal+DSA_SHA1 (biểu diễn chuẩn)
   - Chứng chỉ KEY với (0,0) dài hơn 4 byte và có thể gây ra vấn đề tương thích
   - Một số triển khai có thể không xử lý đúng các chứng chỉ KEY (0,0)

2. **Xác minh dữ liệu dư thừa:**
   - Các triển khai PHẢI xác minh độ dài chứng chỉ khớp với độ dài mong đợi cho các loại khóa
   - Từ chối các chứng chỉ có dữ liệu dư thừa không tương ứng với các loại khóa
   - Cấm dữ liệu rác ở phần cuối sau cấu trúc chứng chỉ hợp lệ

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Ánh xạ

**Mô tả:** Tập hợp thuộc tính khóa–giá trị dùng cho cấu hình và siêu dữ liệu.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Giới hạn kích thước:** - Độ dài khóa: 0-255 byte (+ 1 byte độ dài) - Độ dài giá trị: 0-255 byte (+ 1 byte độ dài) - Tổng kích thước ánh xạ: 0-65535 byte (+ 2 byte trường kích thước) - Kích thước cấu trúc tối đa: 65537 byte

**Yêu cầu sắp xếp quan trọng:**

Khi các ánh xạ xuất hiện trong **cấu trúc đã ký** (RouterInfo, RouterAddress, các thuộc tính Destination, I2CP SessionConfig), các mục PHẢI được sắp xếp theo khóa để đảm bảo tính bất biến của chữ ký:

1. **Phương thức sắp xếp:** Thứ tự từ điển dựa trên giá trị điểm mã Unicode (tương đương với Java String.compareTo())
2. **Phân biệt chữ hoa/thường:** Khóa và giá trị nói chung phân biệt chữ hoa/thường (tùy thuộc vào ứng dụng)
3. **Khóa trùng lặp:** KHÔNG được phép trong các cấu trúc đã ký (sẽ gây lỗi xác minh chữ ký)
4. **Mã hóa ký tự:** So sánh ở cấp độ byte theo UTF-8

**Tại sao sắp xếp quan trọng:** - Chữ ký số được tính trên biểu diễn ở dạng byte - Các thứ tự khóa khác nhau tạo ra các chữ ký số khác nhau - Các ánh xạ không được ký không cần phải sắp xếp nhưng nên tuân theo cùng một quy ước

**Ghi chú triển khai:**

1. **Dư thừa trong mã hóa:**
   - Cả dấu phân cách `=` và `;` VÀ các byte độ dài chuỗi đều hiện diện
   - Điều này kém hiệu quả nhưng được duy trì để đảm bảo tương thích
   - Các byte độ dài có tính quyết định; các dấu phân cách là bắt buộc nhưng dư thừa

2. **Hỗ trợ ký tự:**
   - Mặc dù tài liệu ghi khác, `=` và `;` VẪN được hỗ trợ bên trong chuỗi (các byte độ dài xử lý việc này)
   - Mã hóa UTF-8 hỗ trợ đầy đủ Unicode
   - **Cảnh báo:** I2CP sử dụng UTF-8, nhưng I2NP trước đây không xử lý UTF-8 đúng cách
   - Hãy dùng ASCII cho các ánh xạ I2NP khi có thể để đạt khả năng tương thích tối đa

3. **Ngữ cảnh đặc biệt:**
   - **RouterInfo/RouterAddress:** PHẢI được sắp xếp, không trùng lặp
   - **I2CP SessionConfig:** PHẢI được sắp xếp, không trùng lặp  
   - **Ánh xạ ứng dụng:** Khuyến nghị sắp xếp nhưng không phải lúc nào cũng bắt buộc

**Ví dụ (tùy chọn RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Đặc tả Cấu trúc Chung

### Khóa và Chứng chỉ

**Mô tả:** Cấu trúc cơ bản kết hợp khóa mã hóa, khóa ký và chứng chỉ. Được dùng như cả RouterIdentity (định danh router) và Destination (đích).

**Cấu trúc:**

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
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Căn chỉnh khóa:** - **Khóa công khai mã hóa:** Căn ở đầu (byte 0) - **Đệm:** Ở giữa (nếu cần) - **Khóa công khai dùng để ký:** Căn ở cuối (byte 256 đến byte 383) - **Chứng chỉ:** Bắt đầu tại byte 384

**Tính toán kích thước:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Hướng dẫn tạo phần đệm ([Đề xuất 161](/vi/proposals/161-ri-dest-padding/))

**Phiên bản triển khai:** 0.9.57 (Tháng 1 năm 2023, phát hành 2.1.0)

**Bối cảnh:** - Đối với các khóa không phải ElGamal+DSA, padding (đệm) có trong cấu trúc cố định 384-byte - Đối với Destination (đích), trường khóa công khai 256-byte đã không được sử dụng kể từ 0.6 (2005) - Padding nên được tạo sao cho có thể nén được mà vẫn bảo đảm an toàn

**Yêu cầu:**

1. **Dữ liệu ngẫu nhiên tối thiểu:**
   - Sử dụng ít nhất 32 byte dữ liệu ngẫu nhiên an toàn về mặt mật mã
   - Điều này cung cấp đủ entropy (mức độ ngẫu nhiên) cho mục đích bảo mật

2. **Chiến lược nén:**
   - Lặp lại 32 byte trên toàn bộ trường đệm/khóa công khai
   - Các giao thức như I2NP Database Store, Streaming SYN, SSU2 handshake sử dụng nén
   - Tiết kiệm băng thông đáng kể mà không làm suy giảm bảo mật

3. **Ví dụ:**

**Định danh Router (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destination (Điểm đích) (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Vì sao cách này hiệu quả:**
   - Hàm băm SHA-256 của toàn bộ cấu trúc vẫn bao gồm toàn bộ entropy (độ ngẫu nhiên)
   - Phân phối DHT (bảng băm phân tán) của cơ sở dữ liệu mạng chỉ phụ thuộc vào hàm băm
   - Khóa ký (32 byte EdDSA/X25519) cung cấp 256 bit entropy
   - Thêm 32 byte dữ liệu ngẫu nhiên lặp lại = 512 bit entropy tổng
   - Vượt mức cần thiết cho độ mạnh mật mã

5. **Ghi chú triển khai:**
   - PHẢI lưu trữ và truyền toàn bộ cấu trúc 387+ byte
   - Băm SHA-256 được tính trên toàn bộ cấu trúc chưa nén
   - Nén được áp dụng ở lớp giao thức (I2NP, Streaming, SSU2)
   - Tương thích ngược với tất cả các phiên bản kể từ 0.6 (2005)

**Tài liệu JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (định danh của router)

**Mô tả:** Xác định duy nhất một router trong mạng I2P. Có cấu trúc giống hệt KeysAndCert.

**Định dạng:** Xem cấu trúc KeysAndCert ở trên

**Yêu cầu hiện tại (tính đến 0.9.58):**

1. **Các kiểu khóa bắt buộc:**
   - **Mã hóa:** X25519 (loại 4, 32 byte)
   - **Ký:** EdDSA_SHA512_Ed25519 (loại 7, 32 byte)
   - **Chứng chỉ:** Chứng chỉ khóa (loại 5)

2. **Các loại khóa đã lỗi thời:**
   - ElGamal (type 0) không còn được dùng cho Router Identities (nhận dạng của router) kể từ 0.9.58
   - DSA_SHA1 (type 0) không còn được dùng cho Router Identities kể từ 0.9.58
   - Những loại này KHÔNG được sử dụng cho router mới

3. **Kích thước điển hình:**
   - X25519 + EdDSA với Chứng chỉ khóa = 391 byte
   - 32 byte khóa công khai X25519
   - 320 byte phần đệm (có thể nén theo [Proposal 161](/vi/proposals/161-ri-dest-padding/))
   - 32 byte khóa công khai EdDSA
   - 7 byte chứng chỉ (tiêu đề 3 byte + 4 byte loại khóa)

**Lịch sử phát triển:** - Trước 0.9.16: luôn dùng chứng chỉ NULL (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: bổ sung hỗ trợ Key Certificate (chứng chỉ khóa) - 0.9.48+: hỗ trợ khóa mã hóa X25519 - 0.9.58+: ElGamal và DSA_SHA1 bị loại bỏ dần

**Khóa Cơ sở dữ liệu mạng:** - RouterInfo được lập chỉ mục bằng giá trị băm SHA-256 của RouterIdentity đầy đủ - Giá trị băm được tính trên toàn bộ cấu trúc 391+ byte (bao gồm cả phần đệm)

**Xem thêm:** - Hướng dẫn tạo padding (phần đệm) ([Proposal 161](/vi/proposals/161-ri-dest-padding/)) - Đặc tả Chứng chỉ khóa ở trên

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Điểm đích

**Mô tả:** Định danh điểm cuối cho việc chuyển phát thông điệp an toàn. Về mặt cấu trúc thì giống hệt KeysAndCert, nhưng có ngữ nghĩa sử dụng khác.

**Định dạng:** Xem cấu trúc KeysAndCert ở trên

**Khác biệt quan trọng so với RouterIdentity (định danh router trong I2P):** - **Trường khóa công khai KHÔNG ĐƯỢC SỬ DỤNG và có thể chứa dữ liệu ngẫu nhiên** - Trường này không được sử dụng kể từ phiên bản 0.6 (2005) - Vốn dùng cho cơ chế mã hóa I2CP-to-I2CP cũ (đã vô hiệu hóa) - Hiện chỉ được dùng làm IV (vector khởi tạo) cho mã hóa LeaseSet đã lỗi thời

**Các khuyến nghị hiện tại:**

1. **Khóa ký:**
   - **Khuyến nghị:** EdDSA_SHA512_Ed25519 (loại 7, 32 byte)
   - Phương án thay thế: các loại ECDSA để tương thích với các phiên bản cũ hơn
   - Tránh: DSA_SHA1 (đã lỗi thời, không khuyến khích)

2. **Khóa mã hóa:**
   - Trường không được sử dụng nhưng bắt buộc phải có
   - **Khuyến nghị:** Điền bằng dữ liệu ngẫu nhiên theo [Proposal 161](/vi/proposals/161-ri-dest-padding/) (có thể nén)
   - Kích thước: Luôn 256 byte (khe ElGamal, dù không dùng cho ElGamal)

3. **Chứng chỉ:**
   - Chứng chỉ NULL cho ElGamal + DSA_SHA1 (chỉ dành cho bản cũ)
   - Chứng chỉ khóa cho tất cả các loại khóa ký khác

**Destination (điểm đích I2P) hiện đại điển hình:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Khóa mã hóa thực tế:** - Khóa mã hóa cho Destination (điểm đích trong I2P) nằm trong **LeaseSet**, không phải trong Destination - LeaseSet chứa các khóa công khai mã hóa hiện tại - Xem đặc tả LeaseSet2 về cách xử lý khóa mã hóa

**Khóa Cơ sở dữ liệu mạng:** - LeaseSet được định danh bằng giá trị băm SHA-256 của Destination đầy đủ - Giá trị băm được tính trên toàn bộ cấu trúc 387+ byte

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Cấu trúc cơ sở dữ liệu mạng

### Lease (bản ghi mô tả tunnel đầu vào và thời điểm hết hạn trong I2P)

**Mô tả:** Cho phép một tunnel cụ thể nhận thông điệp cho một Destination (điểm đích trong I2P). Là một phần của định dạng LeaseSet ban đầu (loại 1).

**Định dạng:**

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

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Tổng kích thước:** 44 byte

**Cách dùng:** - Chỉ dùng trong LeaseSet gốc (loại 1, đã lỗi thời) - Đối với LeaseSet2 và các biến thể về sau, hãy dùng Lease2 thay thế

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Loại 1)

**Mô tả:** Định dạng LeaseSet ban đầu. Chứa các tunnel được ủy quyền và các khóa cho một Destination (điểm đích). Được lưu trong cơ sở dữ liệu mạng. **Trạng thái: Đã ngừng sử dụng** (hãy dùng LeaseSet2 thay thế).

**Cấu trúc:**

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

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Lưu trữ cơ sở dữ liệu:** - **Loại cơ sở dữ liệu:** 1 - **Khóa:** băm SHA-256 của Destination (đích đến) - **Giá trị:** cấu trúc LeaseSet đầy đủ

**Các lưu ý quan trọng:**

1. **Khóa công khai của Destination (địa chỉ đích trong I2P) không được sử dụng:**
   - Trường khóa công khai mã hóa trong Destination không được sử dụng
   - Khóa mã hóa trong LeaseSet mới là khóa mã hóa thực tế

2. **Khóa tạm thời:**
   - `encryption_key` là tạm thời (được tạo lại khi router khởi động)
   - `signing_key` là tạm thời (được tạo lại khi router khởi động)
   - Không có khóa nào được lưu giữ qua các lần khởi động lại

3. **Thu hồi (Chưa triển khai):**
   - `signing_key` được dự định dùng cho việc thu hồi LeaseSet
   - Cơ chế thu hồi chưa bao giờ được triển khai
   - Zero-lease LeaseSet (LeaseSet với số lượng lease bằng 0) được dự định dùng cho việc thu hồi nhưng không được sử dụng

4. **Phiên bản/Dấu thời gian:**
   - LeaseSet không có trường dấu thời gian `published` tường minh
   - Phiên bản là thời điểm hết hạn sớm nhất của tất cả các lease (bản ghi thuê đường hầm)
   - LeaseSet mới phải có thời điểm hết hạn của lease sớm hơn để được chấp nhận

5. **Công bố thời điểm hết hạn lease (mục thuê đường hầm trong I2P):**
   - Trước 0.9.7: Tất cả các lease được công bố với cùng thời điểm hết hạn (sớm nhất)
   - 0.9.7+: Công bố thời điểm hết hạn thực tế cho từng lease
   - Đây là chi tiết triển khai, không phải một phần của đặc tả

6. **Không có Lease:**
   - LeaseSet với số Lease (mục chỉ đường hầm trong LeaseSet) bằng 0 vẫn được phép về mặt kỹ thuật
   - Dự định dùng để thu hồi (chưa được triển khai)
   - Không được sử dụng trong thực tế
   - Các biến thể LeaseSet2 yêu cầu ít nhất một Lease

**Ngưng dùng:** LeaseSet loại 1 không còn được khuyến nghị. Các triển khai mới nên dùng **LeaseSet2 (type 3)**, cung cấp:
- Trường dấu thời gian xuất bản (quản lý phiên bản tốt hơn)
- Hỗ trợ nhiều khóa mã hóa
- Khả năng ký ngoại tuyến
- Thời điểm hết hạn lease (thời hạn sử dụng tunnel) 4 byte (so với 8 byte)
- Tùy chọn linh hoạt hơn

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Các biến thể LeaseSet

### Lease2 (bản ghi Lease phiên bản 2 trong I2P)

**Mô tả:** Định dạng lease (bản ghi tuyến có thời hạn trong leaseSet) được cải tiến với trường hết hạn 4 byte. Được sử dụng trong LeaseSet2 (type 3) và MetaLeaseSet (type 7).

**Giới thiệu:** Phiên bản 0.9.38 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Định dạng:**

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

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Tổng kích thước:** 40 byte (nhỏ hơn 4 byte so với Lease gốc)

**So sánh với Lease gốc:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**Tài liệu JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### OfflineSignature (chữ ký ngoại tuyến)

**Mô tả:** Cấu trúc tùy chọn dành cho các khóa tạm thời đã được ký trước, cho phép công bố LeaseSet mà không cần truy cập trực tuyến vào khóa ký riêng tư của Destination (đích trong I2P).

**Giới thiệu:** Phiên bản 0.9.38 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Định dạng:**

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

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Mục đích:** - Cho phép tạo LeaseSet ngoại tuyến - Bảo vệ khóa chính của Destination khỏi bị lộ trực tuyến - Khóa tạm thời có thể bị thu hồi bằng cách công bố LeaseSet mới mà không cần chữ ký ngoại tuyến

**Các kịch bản sử dụng:**

1. **Các đích bảo mật cao:**
   - Khóa ký chính được lưu trữ ngoại tuyến (HSM (mô-đun bảo mật phần cứng), lưu trữ lạnh)
   - Các khóa tạm thời được tạo ngoại tuyến trong các khoảng thời gian giới hạn
   - Khóa tạm thời bị xâm phạm không làm lộ khóa chính

2. **Công bố LeaseSet được mã hóa:**
   - EncryptedLeaseSet có thể bao gồm chữ ký ngoại tuyến
   - Khóa công khai được làm mù (blinded public key) + chữ ký ngoại tuyến cung cấp bảo mật bổ sung

**Các cân nhắc về bảo mật:**

1. **Quản lý thời hạn:**
   - Đặt thời hạn hợp lý (từ ngày đến tuần, không phải năm)
   - Tạo khóa tạm thời mới trước khi hết hạn
   - Thời hạn ngắn hơn = bảo mật tốt hơn, cần bảo trì nhiều hơn

2. **Tạo khóa:**
   - Tạo các khóa tạm thời ngoại tuyến trong môi trường an toàn
   - Ký bằng khóa chủ ngoại tuyến
   - Chỉ truyền khóa tạm thời đã được ký + chữ ký đến router trực tuyến

3. **Thu hồi:**
   - Công bố LeaseSet mới không có chữ ký ngoại tuyến để ngầm thu hồi
   - Hoặc công bố LeaseSet mới với khóa tạm thời khác

**Xác minh chữ ký:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Ghi chú triển khai:** - Tổng kích thước thay đổi tùy theo sigtype (kiểu chữ ký) và loại khóa ký của Destination (đích trong I2P) - Kích thước tối thiểu: 4 + 2 + 32 (khóa EdDSA) + 64 (chữ ký EdDSA) = 102 byte - Kích thước tối đa thực tế: ~600 byte (khóa tạm thời RSA-4096 + chữ ký RSA-4096)

**Tương thích với:** - LeaseSet2 (loại 3) - EncryptedLeaseSet (loại 5) - MetaLeaseSet (loại 7)

**Xem thêm:** [Đề xuất 123](/proposals/123-new-netdb-entries/) để biết chi tiết về giao thức chữ ký ngoại tuyến.

---

### LeaseSet2Header (phần tiêu đề của LeaseSet2)

**Mô tả:** Cấu trúc phần đầu dùng chung cho LeaseSet2 (kiểu 3) và MetaLeaseSet (kiểu 7).

**Giới thiệu:** Phiên bản 0.9.38 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Định dạng:**

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

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Kích thước tổng tối thiểu:** 395 byte (không tính chữ ký ngoại tuyến)

**Định nghĩa các cờ (thứ tự bit: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Chi tiết về cờ:**

**Bit 0 - Khóa ngoại tuyến:** - `0`: Không có chữ ký ngoại tuyến, dùng khóa ký của Destination (điểm đích trong I2P) để xác minh chữ ký LeaseSet - `1`: Cấu trúc OfflineSignature theo sau trường cờ

**Bit 1 - Chưa công bố:** - `0`: LeaseSet đã được công bố theo chuẩn, nên được phát tán tới các floodfills - `1`: LeaseSet chưa công bố (chỉ phía máy khách)   - KHÔNG được phát tán, công bố, hoặc gửi để phản hồi các truy vấn   - Nếu hết hạn, KHÔNG truy vấn netdb để thay thế (trừ khi bit 2 cũng được đặt)   - Dùng cho tunnels cục bộ hoặc thử nghiệm

**Bit 2 - Blinded (kể từ 0.9.42):** - `0`: LeaseSet tiêu chuẩn - `1`: LeaseSet chưa mã hóa này sẽ được blinded (làm mù để ẩn danh) và mã hóa khi công bố   - Phiên bản được công bố sẽ là EncryptedLeaseSet (loại 5)   - Nếu hết hạn, truy vấn **blinded location** trong netdb để thay thế   - Cũng phải đặt bit 1 thành 1 (không công bố + blinded)   - Dùng cho các dịch vụ ẩn được mã hóa

**Giới hạn hết hạn:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Yêu cầu về dấu thời gian xuất bản:**

LeaseSet (type 1) không có trường `published`, khiến phải tìm thời điểm hết hạn sớm nhất của lease (bản ghi đường hầm) để xác định phiên bản. LeaseSet2 bổ sung dấu thời gian `published` tường minh với độ phân giải 1 giây.

**Lưu ý triển khai quan trọng:** - Routers PHẢI áp dụng giới hạn tốc độ cho việc công bố LeaseSet xuống **chậm hơn rất nhiều so với một lần mỗi giây** cho mỗi Destination (đích) - Nếu công bố nhanh hơn, đảm bảo mỗi LeaseSet mới có thời điểm `published` muộn hơn ít nhất 1 giây - Floodfills sẽ từ chối LeaseSet nếu thời điểm `published` không mới hơn phiên bản hiện tại - Khoảng thời gian tối thiểu khuyến nghị: 10-60 giây giữa các lần công bố

**Ví dụ tính toán:**

**LeaseSet2 (tối đa 11 phút):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (tối đa 18,2 giờ):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Phiên bản hóa:** - LeaseSet được coi là "mới hơn" nếu dấu thời gian `published` lớn hơn - Floodfills chỉ lưu trữ và phát tán phiên bản mới nhất - Cần lưu ý khi Lease (bản ghi trong LeaseSet) cũ nhất trùng với Lease cũ nhất của LeaseSet trước đó

---

### LeaseSet2 (Loại 3)

**Mô tả:** Định dạng LeaseSet hiện đại với nhiều khóa mã hóa, chữ ký ngoại tuyến và các bản ghi dịch vụ. Tiêu chuẩn hiện tại cho các dịch vụ ẩn của I2P.

**Giới thiệu:** Phiên bản 0.9.38 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Cấu trúc:**

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

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Lưu trữ cơ sở dữ liệu:** - **Loại cơ sở dữ liệu:** 3 - **Khóa:** Băm SHA-256 của Destination (đích) - **Giá trị:** Cấu trúc LeaseSet2 đầy đủ

**Tính toán chữ ký số:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Thứ tự ưu tiên khóa mã hóa

**Đối với LeaseSet được công bố (máy chủ):** - Các khóa được liệt kê theo thứ tự ưu tiên của máy chủ (ưu tiên cao nhất trước) - Các máy khách hỗ trợ nhiều loại NÊN tuân theo ưu tiên của máy chủ - Chọn loại được hỗ trợ đầu tiên trong danh sách - Nói chung, các loại khóa có số thứ tự cao hơn (mới hơn) bảo mật/hiệu quả hơn - Thứ tự khuyến nghị: Liệt kê các khóa theo thứ tự ngược theo mã loại (mới nhất trước)

**Ví dụ về tùy chọn máy chủ:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Đối với LeaseSet chưa công bố (máy khách):** - Về cơ bản, thứ tự khóa không quan trọng (hiếm khi có kết nối được thực hiện tới máy khách) - Tuân theo cùng quy ước để nhất quán

**Chọn khóa phía client:** - Tuân theo ưu tiên của máy chủ (chọn loại được hỗ trợ đầu tiên) - Hoặc dùng ưu tiên do triển khai quy định - Hoặc xác định ưu tiên kết hợp dựa trên khả năng của cả hai bên

### Ánh xạ tùy chọn

**Yêu cầu:** - Các tùy chọn PHẢI được sắp xếp theo khóa (thứ tự từ điển, thứ tự byte UTF-8) - Việc sắp xếp đảm bảo tính bất biến của chữ ký - KHÔNG cho phép khóa trùng lặp

**Định dạng chuẩn ([Đề xuất 167](/proposals/167-service-records/)):**

Kể từ API 0.9.66 (tháng 6 năm 2025, bản phát hành 2.9.0), các tùy chọn bản ghi dịch vụ tuân theo một định dạng chuẩn hóa. Xem [Đề xuất 167](/proposals/167-service-records/) để biết đặc tả đầy đủ.

**Định dạng tùy chọn bản ghi dịch vụ:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Ví dụ về bản ghi dịch vụ:**

**1. Máy chủ SMTP tự tham chiếu:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Một máy chủ SMTP bên ngoài:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Nhiều máy chủ SMTP (cân bằng tải):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Dịch vụ HTTP với tùy chọn ứng dụng:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Khuyến nghị TTL:** - Tối thiểu: 86400 giây (1 ngày) - TTL dài hơn giúp giảm tải truy vấn netdb - Cân bằng giữa việc giảm số truy vấn và việc lan truyền cập nhật dịch vụ - Đối với dịch vụ ổn định: 604800 (7 ngày) hoặc lâu hơn

**Ghi chú triển khai:**

1. **Khóa mã hóa (tính đến phiên bản 0.9.44):**
   - ElGamal (loại 0, 256 byte): Tương thích với hệ thống cũ
   - X25519 (loại 4, 32 byte): Tiêu chuẩn hiện tại
   - Các biến thể MLKEM: Post-quantum (mật mã hậu lượng tử) (beta, chưa hoàn thiện)

2. **Xác thực độ dài khóa:**
   - Floodfills và máy khách PHẢI có khả năng phân tích cú pháp các loại khóa không xác định
   - Sử dụng trường keylen để bỏ qua các khóa không xác định
   - Không được lỗi khi phân tích cú pháp nếu loại khóa không xác định

3. **Dấu thời gian công bố:**
   - Xem các ghi chú về giới hạn tần suất trong LeaseSet2Header
   - Khoảng cách tối thiểu 1 giây giữa các lần công bố
   - Khuyến nghị: 10-60 giây giữa các lần công bố

4. **Chuyển đổi loại mã hóa:**
   - Hỗ trợ nhiều khóa để cho phép chuyển đổi dần dần
   - Liệt kê cả khóa cũ và khóa mới trong giai đoạn chuyển đổi
   - Gỡ bỏ khóa cũ sau khi đã có đủ thời gian để các ứng dụng khách (client) nâng cấp

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease

**Mô tả:** Cấu trúc Lease cho MetaLeaseSet (LeaseSet dạng meta) có thể tham chiếu các LeaseSet khác thay vì tunnels. Được dùng để cân bằng tải và dự phòng.

**Giới thiệu:** Phiên bản 0.9.38, dự kiến bắt đầu hoạt động từ 0.9.40 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Định dạng:**

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

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Tổng kích thước:** 40 byte

**Loại mục (các bit cờ 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Các kịch bản sử dụng:**

1. **Cân bằng tải:**
   - MetaLeaseSet (tập các MetaLease) với nhiều mục MetaLease
   - Mỗi mục trỏ tới một LeaseSet2 (LeaseSet phiên bản 2) khác nhau
   - Các client chọn dựa trên cost field (trường chi phí)

2. **Dự phòng:**
   - Nhiều mục trỏ tới các LeaseSets (tập thông tin dùng để định tuyến đến một dịch vụ trong I2P) dự phòng
   - Phương án dự phòng nếu LeaseSet chính không khả dụng

3. **Di chuyển dịch vụ:**
   - MetaLeaseSet (cấu trúc siêu dữ liệu tham chiếu tới các LeaseSet) trỏ tới LeaseSet mới
   - Cho phép chuyển đổi mượt mà giữa các Destination (địa chỉ đích trong I2P)

**Cách sử dụng trường Cost:** - Cost thấp = ưu tiên cao hơn - Cost 0 = ưu tiên cao nhất - Cost 255 = ưu tiên thấp nhất - Các client NÊN ưu tiên các mục có Cost thấp hơn - Các mục có Cost bằng nhau có thể được cân bằng tải ngẫu nhiên

**So sánh với Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Loại 7)

**Mô tả:** Biến thể LeaseSet chứa các mục MetaLease (kiểu bản ghi dùng để tạo liên kết gián tiếp tới các LeaseSet khác). Được dùng cho cân bằng tải, dự phòng và di chuyển dịch vụ.

**Giới thiệu:** Được định nghĩa trong 0.9.38, dự kiến hoạt động từ 0.9.40 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Trạng thái:** Đặc tả đã hoàn tất. Cần xác minh tình trạng triển khai trong môi trường sản xuất bằng cách đối chiếu với các bản phát hành I2P hiện tại.

**Cấu trúc:**

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

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Lưu trữ cơ sở dữ liệu:** - **Loại cơ sở dữ liệu:** 7 - **Khóa:** băm SHA-256 của Destination (định danh đích trong I2P) - **Giá trị:** Cấu trúc MetaLeaseSet hoàn chỉnh

**Tính toán chữ ký số:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Kịch bản sử dụng:**

**1. Cân bằng tải:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Chuyển đổi dự phòng:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Di chuyển dịch vụ:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Kiến trúc đa tầng:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Danh sách thu hồi:**

Danh sách thu hồi cho phép MetaLeaseSet thu hồi rõ ràng các LeaseSets đã được công bố trước đó:

- **Mục đích:** Đánh dấu các Destination (đích) cụ thể là không còn hợp lệ
- **Nội dung:** Các băm SHA-256 của các cấu trúc Destination đã bị thu hồi
- **Cách dùng:** Các máy khách KHÔNG ĐƯỢC sử dụng các LeaseSets có băm Destination xuất hiện trong danh sách thu hồi
- **Giá trị điển hình:** Trống (numr=0) trong hầu hết các triển khai

**Ví dụ về thu hồi:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Xử lý hết hạn:**

MetaLeaseSet (tập leaseSet tổng hợp) sử dụng LeaseSet2Header (phần header của LeaseSet2) với giá trị tối đa expires=65535 seconds (~18,2 giờ):

- Dài hơn nhiều so với LeaseSet2 (tối đa ~11 phút)
- Phù hợp cho cơ chế trỏ gián tiếp tương đối tĩnh
- Các LeaseSet được tham chiếu có thể có thời gian hết hạn ngắn hơn
- Các client phải kiểm tra thời gian hết hạn của cả MetaLeaseSet VÀ các LeaseSet được tham chiếu

**Ánh xạ tùy chọn:**

- Sử dụng cùng định dạng như các tùy chọn của LeaseSet2
- Có thể bao gồm service records (bản ghi dịch vụ) ([Proposal 167](/proposals/167-service-records/))
- PHẢI được sắp xếp theo khóa
- Service records thường mô tả dịch vụ cuối cùng, không phải cấu trúc gián tiếp

**Ghi chú triển khai phía máy khách:**

1. **Quy trình phân giải:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Bộ nhớ đệm:**
   - Lưu đệm cả MetaLeaseSet (tập LeaseSet tổng hợp) và các LeaseSet được tham chiếu
   - Kiểm tra hết hạn ở cả hai cấp
   - Theo dõi việc công bố MetaLeaseSet được cập nhật

3. **Chuyển đổi dự phòng:**
   - Nếu mục nhập ưu tiên gặp lỗi, hãy thử mục nhập có chi phí thấp tiếp theo
   - Cân nhắc đánh dấu các mục nhập lỗi là tạm thời không khả dụng
   - Kiểm tra lại định kỳ để xem đã phục hồi chưa

**Tình trạng triển khai:**

[Đề xuất 123](/proposals/123-new-netdb-entries/) cho biết một số phần vẫn "đang trong quá trình phát triển." Người triển khai nên: - Xác minh mức độ sẵn sàng cho môi trường sản xuất trong phiên bản I2P mục tiêu - Kiểm thử hỗ trợ MetaLeaseSet (một biến thể tổng hợp của leaseSet) trước khi triển khai - Kiểm tra xem có đặc tả được cập nhật trong các bản phát hành I2P mới hơn hay không

**Tài liệu JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Loại 5)

**Mô tả:** LeaseSet được mã hóa và làm mù để tăng cường quyền riêng tư. Chỉ có khóa công khai đã làm mù và siêu dữ liệu được hiển thị; các lease thực và khóa mã hóa đều được mã hóa.

**Giới thiệu:** Được định nghĩa từ 0.9.38, hoạt động từ 0.9.39 (xem [Đề xuất 123](/proposals/123-new-netdb-entries/))

**Cấu trúc:**

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

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Lưu trữ cơ sở dữ liệu:** - **Loại cơ sở dữ liệu:** 5 - **Khóa:** băm SHA-256 của **blinded Destination** (Destination được che giấu danh tính; không phải Destination gốc) - **Giá trị:** Cấu trúc EncryptedLeaseSet đầy đủ

**Những điểm khác biệt quan trọng so với LeaseSet2:**

1. **KHÔNG sử dụng cấu trúc LeaseSet2Header** (có các trường tương tự nhưng bố cục khác)
2. **Blinded public key** (khóa công khai được làm mù) thay vì Destination đầy đủ
3. **Tải trọng được mã hóa** thay vì các leases và các khóa ở dạng rõ (cleartext)
4. **Khóa cơ sở dữ liệu là băm (hash) của Destination đã làm mù**, không phải Destination gốc

**Tính toán chữ ký:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Yêu cầu về loại chữ ký:**

**BẮT BUỘC sử dụng RedDSA_SHA512_Ed25519 (loại 11):** - khóa công khai blinded (che mù) 32 byte - chữ ký 64 byte - Cần thiết để đảm bảo các thuộc tính bảo mật liên quan đến blinding - Xem [Đặc tả Red25519](//docs/specs/red25519-signature-scheme/

**Những khác biệt chính so với EdDSA:** - Khóa riêng được tạo bằng phép giảm modulo (không dùng clamping (kẹp bit)) - Chữ ký bao gồm 80 byte dữ liệu ngẫu nhiên - Sử dụng trực tiếp khóa công khai (không dùng giá trị băm) - Cho phép thao tác làm mù an toàn (blinding)

**Blinding (kỹ thuật làm mù trong mật mã) và Mã hóa:**

Xem [Đặc tả EncryptedLeaseSet](/docs/specs/encryptedleaseset/) để biết thông tin chi tiết đầy đủ:

**1. Làm mù khóa:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Vị trí cơ sở dữ liệu:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Các lớp mã hóa (Ba lớp):**

**Lớp 1 - Lớp xác thực (Truy cập của client):** - Mã hóa: mã dòng ChaCha20 - Dẫn xuất khóa: HKDF với bí mật riêng cho từng client - Các client đã xác thực có thể giải mã lớp bên ngoài

**Lớp 2 - Lớp mã hóa:** - Mã hóa: ChaCha20 - Khóa: Được dẫn xuất từ DH (trao đổi khóa Diffie–Hellman) giữa máy khách và máy chủ - Chứa LeaseSet2 hoặc MetaLeaseSet thực tế

**Lớp 3 - LeaseSet bên trong:** - Bản đầy đủ của LeaseSet2 hoặc MetaLeaseSet - Bao gồm tất cả các tunnels, khóa mã hóa, tùy chọn - Chỉ có thể truy cập sau khi giải mã thành công

**Dẫn xuất khóa mã hóa:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Quy trình khám phá:**

**Dành cho các máy khách được ủy quyền:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Đối với các máy khách không được ủy quyền:** - Không thể giải mã ngay cả khi họ tìm thấy EncryptedLeaseSet - Không thể xác định Destination (điểm đích trong I2P) gốc từ phiên bản đã được blinding (làm mù) - Không thể liên kết các EncryptedLeaseSet qua các chu kỳ blinding khác nhau (xoay vòng hàng ngày)

**Thời gian hết hạn:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Dấu thời gian xuất bản:**

Các yêu cầu tương tự như LeaseSet2Header (phần tiêu đề của LeaseSet2): - Phải tăng thêm ít nhất 1 giây giữa các lần công bố - Floodfills từ chối nếu không mới hơn phiên bản hiện tại - Khuyến nghị: 10-60 giây giữa các lần công bố

**Chữ ký ngoại tuyến với LeaseSets được mã hóa:**

Các cân nhắc đặc biệt khi sử dụng chữ ký ngoại tuyến: - Khóa công khai được làm mù được xoay hằng ngày - Chữ ký ngoại tuyến phải được tạo lại hằng ngày với khóa làm mù mới - HOẶC sử dụng chữ ký ngoại tuyến trên LeaseSet bên trong, không phải EncryptedLeaseSet (LeaseSet được mã hóa) bên ngoài - Xem ghi chú của [Đề xuất 123](/proposals/123-new-netdb-entries/)

**Ghi chú triển khai:**

1. **Ủy quyền máy khách:**
   - Có thể ủy quyền nhiều máy khách bằng các khóa khác nhau
   - Mỗi máy khách được ủy quyền có thông tin xác thực giải mã riêng biệt
   - Thu hồi quyền của máy khách bằng cách thay đổi các khóa ủy quyền

2. **Xoay vòng khóa hằng ngày:**
   - Các khóa bị làm mù thay đổi vào nửa đêm theo UTC
   - Máy khách phải tính toán lại Destination (điểm đích) bị làm mù hằng ngày
   - Các EncryptedLeaseSets cũ trở nên không thể được phát hiện sau khi xoay vòng

3. **Thuộc tính quyền riêng tư:**
   - Floodfills không thể xác định Destination gốc (đích dịch vụ I2P)
   - Các máy khách không được ủy quyền không thể truy cập dịch vụ
   - Các giai đoạn blinding (làm mù) khác nhau không thể liên kết với nhau
   - Không có siêu dữ liệu dạng rõ ngoài các thời điểm hết hạn

4. **Hiệu năng:**
   - Máy khách phải thực hiện phép tính blinding (kỹ thuật làm mù trong mật mã) hằng ngày
   - Mã hóa ba lớp làm tăng chi phí tính toán
   - Cân nhắc lưu đệm LeaseSet bên trong đã được giải mã

**Các cân nhắc bảo mật:**

1. **Quản lý khóa ủy quyền:**
   - Phân phối an toàn thông tin xác thực ủy quyền của máy khách
   - Sử dụng thông tin xác thực duy nhất cho mỗi máy khách để thu hồi chi tiết
   - Xoay vòng khóa ủy quyền theo định kỳ

2. **Đồng bộ hóa thời gian:**
   - Blinding hằng ngày (blinding: kỹ thuật “làm mù” để che giấu định danh) phụ thuộc vào ngày UTC được đồng bộ hóa
   - Độ lệch đồng hồ có thể gây lỗi tra cứu
   - Cân nhắc hỗ trợ blinding của ngày trước/tiếp theo để tăng khả năng chịu sai lệch

3. **Rò rỉ siêu dữ liệu:**
   - Các trường Published và expires ở dạng rõ (không mã hóa)
   - Phân tích mẫu có thể để lộ các đặc điểm của dịch vụ
   - Nếu lo ngại, hãy ngẫu nhiên hóa các khoảng thời gian công bố

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Cấu trúc Router

### Địa chỉ router

**Mô tả:** Định nghĩa thông tin kết nối cho một router thông qua một giao thức truyền tải cụ thể.

**Định dạng:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**NGHIÊM TRỌNG - Trường hết hạn:**

⚠️ **Trường hết hạn PHẢI được đặt thành toàn số 0 (8 byte số 0).**

- **Lý do:** Kể từ bản phát hành 0.9.3, thời gian hết hạn khác 0 gây lỗi xác minh chữ ký
- **Lịch sử:** Ban đầu trường hết hạn không được sử dụng, luôn là null
- **Tình trạng hiện tại:** Trường đã được nhận diện lại kể từ 0.9.12, nhưng phải chờ nâng cấp mạng
- **Triển khai:** Luôn đặt thành 0x0000000000000000

Bất kỳ thời điểm hết hạn khác 0 nào cũng sẽ khiến việc xác minh chữ ký của RouterInfo (thông tin router) thất bại.

### Các giao thức truyền tải

**Các giao thức hiện tại (tính đến phiên bản 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Các giá trị kiểu Transport:** - `"SSU2"`: Transport dựa trên UDP hiện hành - `"NTCP2"`: Transport dựa trên TCP hiện hành - `"NTCP"`: Lỗi thời, đã bị loại bỏ (không sử dụng) - `"SSU"`: Lỗi thời, đã bị loại bỏ (không sử dụng)

### Tùy chọn chung

Tất cả các giao thức truyền tải thường bao gồm:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Các tùy chọn dành riêng cho SSU2

Xem [đặc tả SSU2](/docs/specs/ssu2/) để biết chi tiết đầy đủ.

**Các tùy chọn bắt buộc:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Tùy chọn không bắt buộc:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Ví dụ SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Các tùy chọn cụ thể cho NTCP2

Xem [Đặc tả NTCP2](/docs/specs/ntcp2/) để biết thông tin chi tiết đầy đủ.

**Tùy chọn bắt buộc:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Các tùy chọn không bắt buộc (từ 0.9.50):**

```
"caps" = Capability string
```
**Ví dụ về RouterAddress NTCP2:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Ghi chú triển khai

1. **Các giá trị chi phí:**
   - UDP (SSU2) thường có chi phí thấp hơn (5-6) nhờ hiệu quả
   - TCP (NTCP2) thường có chi phí cao hơn (10-11) do overhead (chi phí phụ trội)
   - Chi phí thấp hơn = phương thức truyền tải được ưu tiên

2. **Nhiều địa chỉ:**
   - Routers có thể công bố nhiều bản ghi RouterAddress
   - Các phương thức truyền tải khác nhau (SSU2 và NTCP2)
   - Các phiên bản IP khác nhau (IPv4 và IPv6)
   - Các ứng dụng khách lựa chọn dựa trên chi phí và khả năng

3. **Tên máy chủ (hostname) so với IP:**
   - Địa chỉ IP được ưu tiên để có hiệu năng tốt hơn
   - Tên máy chủ (hostname) được hỗ trợ nhưng làm tăng chi phí tra cứu DNS
   - Cân nhắc dùng IP cho các RouterInfos (RouterInfo: thông tin về router trong I2P) được công bố

4. **Mã hóa Base64:**
   - Tất cả khóa và dữ liệu nhị phân được mã hóa bằng Base64
   - Base64 tiêu chuẩn (RFC 4648)
   - Không có padding hoặc ký tự không tiêu chuẩn

**JavaDoc (tài liệu API Java):** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (thông tin về router)

**Mô tả:** Thông tin được công bố đầy đủ về một router, được lưu trữ trong cơ sở dữ liệu mạng. Bao gồm danh tính, địa chỉ và khả năng.

**Định dạng:**

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
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
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

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Lưu trữ cơ sở dữ liệu:** - **Loại cơ sở dữ liệu:** 0 - **Khóa:** băm SHA-256 của RouterIdentity - **Giá trị:** Cấu trúc RouterInfo đầy đủ

**Dấu thời gian xuất bản:** - Kiểu Date 8 byte (mili giây kể từ epoch) - Dùng cho quản lý phiên bản RouterInfo - Các router công bố RouterInfo mới theo định kỳ - Các floodfill giữ phiên bản mới nhất dựa trên dấu thời gian đã xuất bản

**Sắp xếp địa chỉ:** - **Trước đây:** Các router rất cũ yêu cầu địa chỉ được sắp xếp theo SHA-256 của dữ liệu của chúng - **Hiện tại:** Không cần sắp xếp, không đáng để triển khai chỉ vì tương thích - Địa chỉ có thể theo bất kỳ thứ tự nào

**Trường kích thước peer (lịch sử):** - **Luôn là 0** trong I2P hiện đại - Được dự định cho các tuyến bị hạn chế (chưa được triển khai) - Nếu được triển khai, sẽ theo sau bởi bấy nhiêu Router Hashes - Một số bản triển khai cũ có thể đã yêu cầu danh sách peer được sắp xếp

**Ánh xạ tùy chọn:**

Các tùy chọn PHẢI được sắp xếp theo khóa. Các tùy chọn tiêu chuẩn bao gồm:

**Tùy chọn khả năng:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Tùy chọn mạng:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Tùy chọn thống kê:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Xem [tài liệu RouterInfo của Cơ sở dữ liệu mạng](/docs/specs/common-structures/#routerInfo) để biết danh sách đầy đủ các tùy chọn tiêu chuẩn.

**Tính toán chữ ký:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**RouterInfo (thông tin về router) hiện đại điển hình:**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Ghi chú hiện thực:**

1. **Nhiều địa chỉ:**
   - Các router thường quảng bá 1-4 địa chỉ
   - Các biến thể IPv4 và IPv6
   - Các giao thức truyền tải SSU2 và/hoặc NTCP2
   - Mỗi địa chỉ độc lập

2. **Phiên bản hóa:**
   - RouterInfo (thông tin mô tả router) mới hơn có dấu thời gian `published` muộn hơn
   - Routers xuất bản lại khoảng mỗi ~2 giờ hoặc khi địa chỉ thay đổi
   - Floodfills chỉ lưu và phát tán phiên bản mới nhất

3. **Thẩm định:**
   - Xác minh chữ ký trước khi chấp nhận RouterInfo
   - Kiểm tra trường expiration là toàn số 0 trong mỗi RouterAddress
   - Xác minh ánh xạ options được sắp xếp theo khóa
   - Kiểm tra loại chứng chỉ và loại khóa là đã biết/được hỗ trợ

4. **Cơ sở dữ liệu mạng (netDb):**
   - Các floodfill lưu trữ RouterInfo được lập chỉ mục theo Hash(RouterIdentity)
   - Được lưu trong ~2 ngày sau lần công bố cuối cùng
   - Các router truy vấn các floodfill để khám phá các router khác

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Ghi chú triển khai

### Thứ tự byte (Endianness — cách sắp xếp byte theo big-endian/little-endian)

**Mặc định: Big-Endian (thứ tự byte mạng)**

Hầu hết các cấu trúc I2P sử dụng thứ tự byte big-endian (byte có trọng số lớn ở trước): - Tất cả các kiểu số nguyên (1-8 byte) - Dấu thời gian ngày giờ - TunnelId - Tiền tố độ dài chuỗi - Các loại và độ dài chứng chỉ - Mã loại khóa - Các trường kích thước ánh xạ

**Ngoại lệ: Little-Endian (thứ tự byte: byte thấp trước)**

Các loại khóa sau sử dụng mã hóa **little-endian** (thứ tự byte nhỏ-đầu): - **X25519** khóa mã hóa (loại 4) - **EdDSA_SHA512_Ed25519** khóa ký (loại 7) - **EdDSA_SHA512_Ed25519ph** khóa ký (loại 8) - **RedDSA_SHA512_Ed25519** khóa ký (loại 11)

**Hiện thực:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Phiên bản hóa cấu trúc

**Không bao giờ giả định kích thước cố định:**

Nhiều cấu trúc có độ dài thay đổi: - RouterIdentity (định danh router): 387+ byte (không phải lúc nào cũng là 387) - Destination (đích đến): 387+ byte (không phải lúc nào cũng là 387) - LeaseSet2 (tập leaseSet phiên bản 2): thay đổi đáng kể - Chứng chỉ: 3+ byte

**Luôn đọc các trường độ dài:** - Độ dài chứng chỉ ở các byte 1-2 - Kích thước mapping (ánh xạ) ở phần đầu - KeysAndCert luôn được tính là 384 + 3 + certificate_length

**Kiểm tra dữ liệu dư thừa:** - Không cho phép dữ liệu rác ở phần đuôi sau các cấu trúc hợp lệ - Xác minh độ dài chứng chỉ khớp với kiểu khóa - Bắt buộc độ dài chính xác như mong đợi cho các kiểu kích thước cố định

### Khuyến nghị hiện tại (Tháng 10 năm 2025)

**Dành cho các định danh Router mới:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/vi/proposals/161-ri-dest-padding/)
```
**Dành cho các điểm đích (Destination) mới:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/vi/proposals/161-ri-dest-padding/)
```
**Đối với LeaseSets mới:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Dành cho các dịch vụ được mã hóa:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Các tính năng đã lỗi thời - Không sử dụng

**Mã hóa đã lỗi thời:** - ElGamal (loại 0) cho Danh tính Router (không còn được khuyến nghị từ 0.9.58) - Mã hóa ElGamal/AES+SessionTag (hãy dùng ECIES-X25519)

**Phương thức ký đã lỗi thời:** - DSA_SHA1 (loại 0) cho định danh Router (được đánh dấu ngừng dùng từ 0.9.58) - Các biến thể ECDSA (các loại 1-3) cho các triển khai mới - Các biến thể RSA (các loại 4-6) ngoại trừ các tệp SU3

**Định dạng mạng đã lỗi thời:** - LeaseSet loại 1 (hãy dùng LeaseSet2) - Lease (44 byte, hãy dùng Lease2) - Định dạng thời điểm hết hạn Lease ban đầu

**Các giao thức truyền tải đã lỗi thời:** - NTCP (đã bị loại bỏ trong 0.9.50) - SSU (đã bị loại bỏ trong 2.4.0)

**Chứng chỉ không còn được khuyến nghị sử dụng:** - HASHCASH (loại 1) - HIDDEN (loại 2) - SIGNED (loại 3) - MULTIPLE (loại 4)

### Các cân nhắc bảo mật

**Sinh khóa:** - Luôn sử dụng bộ sinh số ngẫu nhiên an toàn về mặt mật mã - Không bao giờ tái sử dụng khóa trong các bối cảnh khác nhau - Bảo vệ khóa riêng tư bằng các cơ chế kiểm soát truy cập phù hợp - Xóa an toàn dữ liệu khóa khỏi bộ nhớ khi hoàn tất

**Xác minh chữ ký:** - Luôn xác minh chữ ký trước khi tin cậy dữ liệu - Kiểm tra độ dài chữ ký khớp với loại khóa - Xác nhận dữ liệu đã ký bao gồm các trường mong đợi - Đối với các ánh xạ đã sắp xếp, hãy kiểm tra thứ tự sắp xếp trước khi ký/xác minh

**Xác thực dấu thời gian:** - Kiểm tra rằng các thời gian được công bố là hợp lý (không quá xa trong tương lai) - Xác thực thời hạn lease (bản ghi đường hầm trong I2P) chưa hết hạn - Cân nhắc dung sai độ lệch đồng hồ (thường ±30 giây)

**Cơ sở dữ liệu mạng:** - Xác thực tất cả các cấu trúc trước khi lưu trữ - Thực thi giới hạn kích thước để ngăn chặn tấn công từ chối dịch vụ (DoS) - Giới hạn tốc độ các truy vấn và việc công bố - Xác minh khóa cơ sở dữ liệu khớp với giá trị băm của cấu trúc

### Ghi chú về khả năng tương thích

**Tương thích ngược:** - ElGamal và DSA_SHA1 vẫn được hỗ trợ cho các routers đời cũ - Các kiểu khóa đã lỗi thời vẫn hoạt động nhưng không được khuyến khích - Đệm có thể nén ([Proposal 161](/vi/proposals/161-ri-dest-padding/)) tương thích ngược đến 0.6

**Tương thích về sau:** - Các loại khóa không xác định có thể được phân tích dựa vào các trường độ dài - Các loại chứng chỉ không xác định có thể được bỏ qua dựa vào độ dài - Các loại chữ ký không xác định nên được xử lý một cách an toàn, không gây lỗi - Các bản triển khai không nên lỗi khi gặp các tính năng tùy chọn không xác định

**Chiến lược di chuyển:** - Hỗ trợ cả các loại khóa cũ và mới trong giai đoạn chuyển đổi - LeaseSet2 có thể liệt kê nhiều khóa mã hóa - Chữ ký ngoại tuyến cho phép xoay vòng khóa an toàn - MetaLeaseSet cho phép di chuyển dịch vụ một cách minh bạch

### Kiểm thử và thẩm định

**Xác thực cấu trúc:** - Xác minh tất cả các trường độ dài nằm trong phạm vi mong đợi - Kiểm tra rằng các cấu trúc có độ dài biến đổi được phân tích cú pháp chính xác - Xác thực rằng chữ ký số được xác minh thành công - Kiểm thử với cả các cấu trúc có kích thước tối thiểu và tối đa

**Các trường hợp biên:** - Chuỗi có độ dài 0 - Ánh xạ rỗng - Số lượng lease (bản ghi lease trong I2P) tối thiểu và tối đa - Chứng chỉ có nội dung độ dài 0 - Các cấu trúc rất lớn (gần kích thước tối đa)

**Khả năng tương tác:** - Kiểm thử đối chiếu với bản triển khai I2P bằng Java chính thức - Xác minh khả năng tương thích với i2pd - Kiểm thử với nhiều nội dung cơ sở dữ liệu mạng khác nhau - Xác thực đối chiếu với các véc-tơ kiểm thử đã biết là đúng

---

## Tài liệu tham khảo

### Đặc tả kỹ thuật

- [Giao thức I2NP](/docs/specs/i2np/)
- [Giao thức I2CP](/docs/specs/i2cp/)
- [Truyền tải SSU2](/docs/specs/ssu2/)
- [Truyền tải NTCP2](/docs/specs/ntcp2/)
- [Giao thức Tunnel](/docs/specs/implementation/)
- [Giao thức Datagram](/docs/api/datagrams/)

### Mật mã học

- [Tổng quan về mật mã học](/docs/specs/cryptography/)
- [Mã hóa ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Mã hóa ECIES-X25519](/docs/specs/ecies/)
- [ECIES cho router](/docs/specs/ecies/#routers)
- [ECIES lai (hậu lượng tử)](/docs/specs/ecies/#hybrid)
- [Chữ ký Red25519](/docs/specs/red25519-signature-scheme/)
- [LeaseSet đã mã hóa](/docs/specs/encryptedleaseset/)

### Các đề xuất

- [Đề xuất 123: Các bản ghi netDB mới](/proposals/123-new-netdb-entries/)
- [Đề xuất 134: Kiểu chữ ký GOST](/proposals/134-gost/)
- [Đề xuất 136: Kiểu chữ ký thử nghiệm](/proposals/136-experimental-sigtypes/)
- [Đề xuất 145: ECIES-P256](/proposals/145-ecies/)
- [Đề xuất 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Đề xuất 161: Sinh phần đệm](/vi/proposals/161-ri-dest-padding/)
- [Đề xuất 167: Bản ghi dịch vụ](/proposals/167-service-records/)
- [Đề xuất 169: Mật mã hậu lượng tử](/proposals/169-pq-crypto/)
- [Chỉ mục tất cả đề xuất](/proposals/)

### Cơ sở dữ liệu mạng

- [Tổng quan về netDb (Cơ sở dữ liệu mạng)](/docs/specs/common-structures/)
- [Tùy chọn tiêu chuẩn của RouterInfo](/docs/specs/common-structures/#routerInfo)

### Tham chiếu API JavaDoc

- [Gói dữ liệu cốt lõi](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Các tiêu chuẩn bên ngoài

- **RFC 7748 (X25519):** Đường cong elliptic cho bảo mật
- **RFC 7539 (ChaCha20):** ChaCha20 và Poly1305 cho các giao thức của IETF
- **RFC 4648 (Base64):** Các dạng mã hóa dữ liệu Base16, Base32 và Base64
- **FIPS 180-4 (SHA-256):** Tiêu chuẩn băm an toàn
- **FIPS 204 (ML-DSA):** Module-Lattice-Based (dựa trên lưới mô-đun) Digital Signature Standard
- [Sổ đăng ký dịch vụ IANA](http://www.dns-sd.org/ServiceTypes.html)

### Tài nguyên cộng đồng

- [Trang web I2P](/)
- [Diễn đàn I2P](https://i2pforum.net)
- [GitLab của I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Bản sao trên GitHub của I2P](https://github.com/i2p/i2p.i2p)
- [Chỉ mục Tài liệu Kỹ thuật](/docs/)

### Thông tin phát hành

- [Bản phát hành I2P 2.10.0](/vi/blog/2025/09/08/i2p-2.10.0-release/)
- [Lịch sử phát hành](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Nhật ký thay đổi](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Phụ lục: Bảng tham khảo nhanh

### Tham khảo nhanh các loại khóa

**Tiêu chuẩn hiện hành (khuyến nghị cho mọi triển khai mới):** - **Mã hóa:** X25519 (loại 4, 32 byte, little-endian (thứ tự byte LSB trước)) - **Ký:** EdDSA_SHA512_Ed25519 (loại 7, 32 byte, little-endian)

**Legacy (được hỗ trợ nhưng không còn được khuyến nghị):** - **Mã hóa:** ElGamal (kiểu 0, 256 byte, big-endian) - **Ký số:** DSA_SHA1 (kiểu 0, khóa riêng 20 byte / khóa công khai 128 byte, big-endian)

**Chuyên biệt:** - **Ký (Encrypted LeaseSet):** RedDSA_SHA512_Ed25519 (kiểu 11, 32 byte, little-endian (thứ tự byte nhỏ-đến-lớn))

**Hậu lượng tử (Beta, chưa hoàn thiện):** - **Mã hóa lai:** các biến thể MLKEM_X25519 (các loại 5-7) - **Mã hóa PQ thuần:** các biến thể MLKEM (chưa được gán mã loại)

### Tham khảo nhanh kích thước cấu trúc

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Tham khảo nhanh các loại cơ sở dữ liệu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Tham khảo nhanh về giao thức vận chuyển

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Tham khảo nhanh các mốc phiên bản

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/vi/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
