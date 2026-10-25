---
title: "Đặc tả I2NP"
description: "Định dạng thông điệp, mức độ ưu tiên và cấu trúc chung của I2P Network Protocol (I2NP) cho giao tiếp giữa các router."
slug: "i2np"
aliases:
  - "/vi/spec/i2np"
  - "/vi/spec/i2np/"
category: "Giao thức"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Tổng quan

I2P Network Protocol (I2NP) là lớp nằm phía trên các giao thức truyền tải I2P. Đây là giao thức router-to-router. Nó được sử dụng để tra cứu và trả lời cơ sở dữ liệu mạng, tạo tunnel, và truyền các thông điệp dữ liệu được mã hóa của router và client. Các thông điệp I2NP có thể được gửi trực tiếp điểm-tới-điểm đến một router khác, hoặc được gửi ẩn danh thông qua các tunnel đến router đó.

## Phiên bản Giao thức {#versions}

Tất cả router phải công bố phiên bản giao thức I2NP của chúng trong trường "router.version" trong các thuộc tính RouterInfo. Trường phiên bản này là phiên bản API, cho biết mức độ hỗ trợ cho các tính năng giao thức I2NP khác nhau, và không nhất thiết là phiên bản router thực tế.

Nếu các router thay thế (không phải Java) muốn công bố bất kỳ thông tin phiên bản nào về triển khai router thực tế, chúng phải thực hiện điều này trong một thuộc tính khác. Các phiên bản khác ngoài những phiên bản được liệt kê bên dưới đều được phép. Hỗ trợ sẽ được xác định thông qua so sánh số; ví dụ, 0.9.13 có nghĩa là hỗ trợ các tính năng của 0.9.12. Lưu ý rằng thuộc tính "coreVersion" không còn được công bố trong thông tin router nữa và chưa bao giờ được sử dụng để xác định phiên bản giao thức I2NP.

Tóm tắt cơ bản về các phiên bản giao thức I2NP như sau. Để biết chi tiết, xem bên dưới.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Lưu ý rằng cũng có các tính năng liên quan đến giao thức vận chuyển và các vấn đề tương thích; xem tài liệu về giao thức vận chuyển NTCP và SSU để biết chi tiết.

## Các Cấu trúc Chung {#structures}

Các cấu trúc sau đây là các thành phần của nhiều thông điệp I2NP. Chúng không phải là các thông điệp hoàn chỉnh.

### Header Tin nhắn I2NP {#struct-I2NPMessageHeader}

#### Mô tả

Header chung cho tất cả các thông điệp I2NP, chứa thông tin quan trọng như checksum, ngày hết hạn, v.v.

#### Nội dung

Có ba định dạng riêng biệt được sử dụng, tùy thuộc vào ngữ cảnh; một định dạng tiêu chuẩn và hai định dạng ngắn.

Định dạng 16 byte tiêu chuẩn chứa 1 byte [Integer](/docs/specs/common-structures/#integer) chỉ định loại thông điệp này, theo sau là 4 byte [Integer](/docs/specs/common-structures/#integer) chỉ định message-id. Sau đó có một [Date](/docs/specs/common-structures/#date) hết hạn, theo sau là 2 byte [Integer](/docs/specs/common-structures/#integer) chỉ định độ dài của message payload, theo sau là một [Hash](/docs/specs/common-structures/#hash) được cắt ngắn về byte đầu tiên. Sau đó là dữ liệu thông điệp thực tế.

Các định dạng ngắn sử dụng thời gian hết hạn 4 byte tính bằng giây thay vì thời gian hết hạn 8 byte tính bằng mili giây. Các định dạng ngắn không chứa checksum hoặc kích thước, những thông tin này được cung cấp bởi các lớp đóng gói, tùy thuộc vào ngữ cảnh.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Ghi chú

- Khi được truyền qua [SSU](/docs/transports/ssu/), header chuẩn 16-byte sẽ không được sử dụng. Chỉ có 1-byte type và 4-byte expiration tính bằng giây được bao gồm. Message id và size được tích hợp trong định dạng gói dữ liệu SSU. Checksum không bắt buộc vì lỗi được phát hiện trong quá trình giải mã.

- Khi được truyền qua [NTCP2](/docs/specs/ntcp2/) hoặc [SSU2](/docs/specs/ssu2/), header tiêu chuẩn 16-byte không được sử dụng. Chỉ bao gồm 1-byte type, 4-byte message id, và 4-byte expiration tính bằng giây. Kích thước được tích hợp trong định dạng gói dữ liệu NTCP2 và SSU2. Checksum không cần thiết vì lỗi được phát hiện trong quá trình giải mã.

- Header tiêu chuẩn cũng được yêu cầu cho các thông điệp I2NP có chứa trong các thông điệp và cấu trúc khác (Data, TunnelData, TunnelGateway, và GarlicClove). Kể từ phiên bản 0.8.12, để giảm overhead, việc xác minh checksum đã bị vô hiệu hóa tại một số vị trí trong protocol stack. Tuy nhiên, để tương thích với các phiên bản cũ hơn, việc tạo checksum vẫn được yêu cầu. Đây là một chủ đề cho nghiên cứu tương lai để xác định các điểm trong protocol stack nơi mà phiên bản router đầu xa đã được biết và việc tạo checksum có thể bị vô hiệu hóa.

- Thời gian hết hạn ngắn không có dấu và sẽ quay vòng vào ngày 7 tháng 2 năm 2106. Kể từ ngày đó, cần phải thêm một offset để có được thời gian chính xác.

- Các triển khai có thể từ chối các thông điệp có thời gian hết hạn quá xa trong tương lai. Thời gian hết hạn tối đa được khuyến nghị là 60 giây trong tương lai.

### BuildRequestRecord {#struct-BuildRequestRecord}

ĐÃ LẠC HẬU, chỉ được sử dụng trong mạng hiện tại khi một tunnel chứa một router ElGamal. Xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Mô tả

Một Record trong một tập hợp nhiều record để yêu cầu tạo một hop trong tunnel. Để biết thêm chi tiết, xem [tổng quan về tunnel](/docs/specs/tunnel-implementation/) và [đặc tả tạo tunnel ElGamal](/docs/specs/tunnel-creation/).

Đối với ECIES-X25519 BuildRequestRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Mục lục (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) để nhận tin nhắn, theo sau là [Hash](/docs/specs/common-structures/#hash) của [RouterIdentity](/docs/specs/common-structures/#routeridentity) của chúng ta. Sau đó là [TunnelId](/docs/specs/common-structures/#tunnelid) và [Hash](/docs/specs/common-structures/#hash) của [RouterIdentity](/docs/specs/common-structures/#routeridentity) của router tiếp theo.

Mã hóa ElGamal và AES:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal mã hóa:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Văn bản rõ:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Ghi chú

- Trong bản ghi mã hóa 512 byte, dữ liệu ElGamal chứa các byte 1-256 và 258-513 của khối mã hóa ElGamal 514 byte [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Hai byte đệm từ khối (các byte zero tại vị trí 0 và 257) được loại bỏ.

- Xem [đặc tả tạo tunnel](/docs/specs/tunnel-creation/) để biết chi tiết về nội dung các trường.

### BuildResponseRecord {#struct-BuildResponseRecord}

ĐÃ BỊ LOẠI BỎ, chỉ được sử dụng trong mạng hiện tại khi tunnel chứa một router ElGamal. Xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Mô tả

Một bản ghi trong tập hợp nhiều bản ghi với các phản hồi cho yêu cầu xây dựng. Để biết thêm chi tiết, xem [tổng quan tunnel](/docs/specs/tunnel-implementation/) và [đặc tả tạo tunnel ElGamal](/docs/specs/tunnel-creation/).

Đối với ECIES-X25519 BuildResponseRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Nội dung (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Ghi chú

- Trường dữ liệu ngẫu nhiên có thể được sử dụng trong tương lai để trả về thông tin tắc nghẽn hoặc kết nối peer cho người yêu cầu.

- Xem [đặc tả tạo tunnel](/docs/specs/tunnel-creation/) để biết chi tiết về trường reply.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Chỉ dành cho các router ECIES-X25519, kể từ phiên bản API 0.9.51. 218 byte khi được mã hóa. Xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Chỉ dành cho router ECIES-X25519, từ phiên bản API 0.9.51. 218 byte khi được mã hóa. Xem [Tạo Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Cảnh báo: Đây là định dạng được sử dụng cho các garlic clove trong các garlic message được mã hóa ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Định dạng cho các garlic message và garlic clove ECIES-AEAD-X25519-Ratchet khác biệt đáng kể; xem [ECIES](/docs/specs/ecies/) để biết đặc tả kỹ thuật.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Ghi chú

- Clove không bao giờ bị phân mảnh. Khi được sử dụng trong Garlic Clove, bit đầu tiên của flag byte Delivery Instructions chỉ định mã hóa. Nếu bit này là 0, clove không được mã hóa. Nếu là 1, clove được mã hóa, và một Session Key 32 byte ngay lập tức theo sau flag byte. Mã hóa clove chưa được triển khai đầy đủ.

- Xem thêm [đặc tả garlic routing](/docs/overview/garlic-routing/).

- Độ dài tối đa là một hàm của tổng độ dài của tất cả các clove và độ dài tối đa của GarlicMessage.

- Trong tương lai, certificate có thể được sử dụng cho HashCash để "trả tiền" cho việc định tuyến.

- Thông điệp có thể là bất kỳ thông điệp I2NP nào (bao gồm cả GarlicMessage, mặc dù không được sử dụng trong thực tế). Các thông điệp được sử dụng trong thực tế là DataMessage, DeliveryStatusMessage, và DatabaseStoreMessage.

- Clove ID thường được đặt thành một số ngẫu nhiên khi truyền và được kiểm tra trùng lặp khi nhận (cùng không gian message ID với Message ID cấp cao nhất)

### Hướng dẫn Giao hàng Garlic Clove {#struct-GarlicCloveDeliveryInstructions}

Đây là định dạng được sử dụng cho cả garlic clove được mã hóa ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) và được mã hóa ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/).

Đặc tả này chỉ dành cho Delivery Instructions bên trong Garlic Cloves. Lưu ý rằng "Delivery Instructions" cũng được sử dụng bên trong Tunnel Messages, nơi định dạng khác biệt đáng kể. Xem [tài liệu Tunnel Message](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) để biết chi tiết. KHÔNG sử dụng đặc tả sau đây cho Tunnel Message Delivery Instructions!

Session key và delay không được sử dụng và không bao giờ có mặt, vì vậy ba độ dài có thể có là 1 (LOCAL), 33 (ROUTER và DESTINATION), và 37 (TUNNEL) byte.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Tin nhắn

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Mô tả

Một lưu trữ cơ sở dữ liệu không được yêu cầu, hoặc phản hồi cho một Thông điệp [DatabaseLookup](#msg-DatabaseLookup) thành công

#### Mục lục

Một LeaseSet, LeaseSet2, MetaLeaseSet, hoặc EncryptedLeaseset không nén, hoặc một RouterInfo đã nén

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Ghi chú

- Vì lý do bảo mật, các trường phản hồi sẽ bị bỏ qua nếu thông điệp được nhận qua tunnel.

- Key là hash "thực" của RouterIdentity hoặc Destination, KHÔNG phải là routing key.

- Các loại 3, 5, và 7 có từ phiên bản 0.9.38. Xem đề xuất 123 để biết thêm thông tin. Các loại này chỉ nên được gửi đến các router có phiên bản 0.9.38 trở lên.

- Như một tối ưu hóa để giảm kết nối, nếu loại là LeaseSet, reply token được bao gồm, reply tunnel ID khác không, và cặp reply gateway/tunnelID được tìm thấy trong LeaseSet như một lease, người nhận có thể chuyển hướng reply đến bất kỳ lease nào khác trong LeaseSet.

- Để ẩn hệ điều hành router và cách triển khai, khớp với việc triển khai gzip của Java router bằng cách đặt thời gian sửa đổi thành 0 và byte OS thành 0xFF, và đặt XFL thành 0x02 (nén tối đa, thuật toán chậm nhất). Xem RFC 1952. 10 byte đầu tiên của thông tin router được nén sẽ là (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Mô tả

Một yêu cầu tìm kiếm một mục trong cơ sở dữ liệu mạng. Phản hồi có thể là [DatabaseStore](#msg-DatabaseStore) hoặc [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Mục lục

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Mã hóa phản hồi

LƯU Ý: Router ElGamal đã bị phản đối kể từ API 0.9.58. Vì phiên bản floodfill tối thiểu được khuyến nghị để truy vấn hiện tại là 0.9.58, các triển khai không cần phải thực hiện mã hóa cho router floodfill ElGamal. Các đích đến ElGamal vẫn được hỗ trợ.

Flag bit 4 được sử dụng kết hợp với bit 1 để xác định chế độ mã hóa phản hồi. Flag bit 4 chỉ được đặt khi gửi đến các router có phiên bản 0.9.46 trở lên. Xem đề xuất 154 và 156 để biết chi tiết.

Trong bảng dưới đây, "DH n/a" có nghĩa là phản hồi không được mã hóa. "DH no" có nghĩa là các khóa phản hồi được bao gồm trong yêu cầu. "DH yes" có nghĩa là các khóa phản hồi được tạo ra từ phép toán DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Không Mã Hóa

reply_key, tags, và reply_tags không có mặt.

#### ElG to ElG

Được hỗ trợ từ phiên bản 0.9.7. Không được khuyến nghị từ phiên bản 0.9.58. Điểm đích ElG gửi một yêu cầu tra cứu đến router ElG.

Tạo khóa người yêu cầu:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Định dạng thông điệp:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES sang ElG

Được hỗ trợ từ phiên bản 0.9.46. Đã không được khuyến khích sử dụng từ phiên bản 0.9.58. Destination ECIES gửi một truy vấn lookup đến một router ElG. Các trường reply_key và reply_tags được định nghĩa lại cho phản hồi được mã hóa ECIES.

Tạo khóa người yêu cầu:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Định dạng thông điệp: Định nghĩa lại các trường reply_key và reply_tags như sau:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
Phản hồi là một thông báo ECIES Existing Session, như được định nghĩa trong [ECIES](/docs/specs/ecies/).

#### Định dạng phản hồi

Đây là thông điệp phiên hiện tại, giống như trong [ECIES](/docs/specs/ecies/), được sao chép bên dưới để tham khảo.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
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
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Tham số AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES đến ECIES (0.9.49)

ECIES destination hoặc router gửi một lookup tới một ECIES router. Được hỗ trợ từ phiên bản 0.9.49.

ECIES router được giới thiệu trong phiên bản 0.9.48, xem [Đề xuất 156](/proposals/156/). ECIES destination và router có thể sử dụng cùng định dạng như trong phần "ECIES to ElG" ở trên, với reply key được bao gồm trong yêu cầu. Mã hóa tin nhắn lookup được chỉ định trong [ECIES-ROUTERS](/docs/specs/ecies-routers/). Người yêu cầu là ẩn danh.

#### ECIES sang ECIES (tương lai)

Tùy chọn này vẫn chưa được định nghĩa đầy đủ. Xem [Đề xuất 156](/proposals/156/).

#### Ghi chú

- Trước phiên bản 0.9.16, khóa có thể dành cho RouterInfo hoặc LeaseSet, vì chúng nằm trong cùng một không gian khóa, và không có cờ nào để yêu cầu chỉ một loại dữ liệu cụ thể.

- Cờ mã hóa, khóa phản hồi và thẻ phản hồi kể từ phiên bản 0.9.7.

- Các phản hồi được mã hóa chỉ hữu ích khi phản hồi được gửi thông qua tunnel.

- Số lượng thẻ được bao gồm có thể lớn hơn một nếu các chiến lược tra cứu DHT thay thế (ví dụ, tra cứu đệ quy) được triển khai.

- Khóa tra cứu và khóa loại trừ là các hash "thực", KHÔNG phải routing key.

- Các loại 3, 5, và 7 có thể được trả về từ phiên bản 0.9.38. Xem đề xuất 123 để biết thêm thông tin.

- Ghi chú về exploratory lookup: Một exploratory lookup được định nghĩa để trả về danh sách các hash không phải floodfill gần với khóa. Tuy nhiên, xem các ghi chú quan trọng cho DatabaseSearchReply về các biến thể triển khai. Thêm vào đó, đặc tả này chưa bao giờ làm rõ liệu bên nhận có nên tra cứu khóa tìm kiếm cho một RI và trả về DatabaseStore thay vì DSRM nếu có. Java có thực hiện tra cứu; i2pd thì không. Do đó, không khuyến nghị sử dụng exploratory lookup cho các hash đã nhận trước đó.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Mô tả

Phản hồi cho một Thông điệp [DatabaseLookup](#msg-DatabaseLookup) thất bại

#### Mục lục

Danh sách các router hash gần nhất với khóa được yêu cầu

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Ghi chú

- Hash 'from' không được xác thực và không thể tin cậy được.

- Các hash peer được trả về không nhất thiết phải gần key hơn so với router đang được truy vấn. Đối với các phản hồi cho các tìm kiếm thông thường, điều này tạo điều kiện cho việc khám phá các floodfill mới và tìm kiếm "ngược" (xa-khỏi-key) để tăng tính mạnh mẽ.

- Khóa cho một exploration lookup thường được tạo ngẫu nhiên. Do đó, các peer_hashes không phải floodfill trong phản hồi có thể được chọn bằng thuật toán tối ưu, chẳng hạn như cung cấp các peer gần với khóa nhưng không nhất thiết là gần nhất trong toàn bộ cơ sở dữ liệu mạng cục bộ, để tránh việc sắp xếp hoặc tìm kiếm không hiệu quả trong toàn bộ cơ sở dữ liệu cục bộ. Các chiến lược khác như bộ nhớ đệm cũng có thể phù hợp. Điều này phụ thuộc vào triển khai.

- Số lượng hash thông thường được trả về: 3

- Số lượng hash tối đa được khuyến nghị để trả về: 16

- Khóa tra cứu, hash của peer, và hash nguồn là các hash "thực", KHÔNG phải routing key.

### DeliveryStatus {#msg-DeliveryStatus}

#### Mô tả

Một xác nhận tin nhắn đơn giản. Thường được tạo bởi người gửi tin nhắn ban đầu, và được đóng gói trong một Garlic Message cùng với chính tin nhắn đó, để được trả về bởi đích đến.

Tin nhắn này cũng được sử dụng để kiểm tra tunnel, trong đó người gửi truyền nó qua một outbound tunnel đến một inbound tunnel, rồi quay ngược trở lại chính nó. Trong trường hợp này, tin nhắn cũng thường được bao bọc bằng garlic encryption. Việc kiểm tra tunnel là bắt buộc kể từ phiên bản API 0.9.68 năm 2026-02, vì các router được phép loại bỏ các tunnel đang tham gia nếu không nhận được lưu lượng nào sau hai phút đầu tiên.

#### Nội dung

ID của tin nhắn đã được gửi và thời gian tạo hoặc thời gian đến.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Ghi chú

- Có vẻ như dấu thời gian luôn được người tạo thiết lập thành thời gian hiện tại. Tuy nhiên có một số cách sử dụng điều này trong code, và có thể sẽ được thêm nhiều hơn trong tương lai.

- Thông điệp này cũng được sử dụng như một xác nhận phiên đã được thiết lập trong SSU [SSU-ED](/docs/transports/ssu/#establishDirect). Trong trường hợp này, ID thông điệp được đặt thành một số ngẫu nhiên, và "thời gian đến" được đặt thành ID toàn mạng hiện tại, là 2 (tức là 0x0000000000000002).

### Garlic {#msg-Garlic}

Cảnh báo: Đây là định dạng được sử dụng cho các tin nhắn tỏi mã hóa ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Định dạng cho các tin nhắn tỏi và tỏi con sử dụng ECIES-AEAD-X25519-Ratchet khác biệt đáng kể; xem [ECIES](/docs/specs/ecies/) để biết thông số kỹ thuật.

#### Mô tả

Được dùng để bao bọc nhiều tin nhắn I2NP được mã hóa

#### Nội dung

Khi được giải mã, một chuỗi các [Garlic Cloves](#struct-GarlicClove) và dữ liệu bổ sung khác, còn được gọi là Clove Set.

Đã mã hóa:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Dữ liệu đã giải mã, còn được gọi là bộ Clove:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Ghi chú

- Khi không được mã hóa, dữ liệu chứa một hoặc nhiều [Garlic Cloves](#struct-GarlicClove).

- Khối mã hóa AES được đệm đến tối thiểu 128 byte; với Session Tag 32 byte thì kích thước tối thiểu của thông điệp mã hóa là 160 byte; với 4 byte độ dài thì kích thước tối thiểu của Garlic Message là 164 byte.

- Độ dài tối đa thực tế nhỏ hơn 64 KB; xem [I2NP](/docs/protocol/i2np/).

- Xem thêm [đặc tả ElGamal/AES](/docs/specs/elgamal-aes/).

- Xem thêm [đặc tả garlic routing](/docs/overview/garlic-routing/).

- Kích thước tối thiểu 128 byte của khối mã hóa AES hiện tại không thể cấu hình được, tuy nhiên kích thước tối thiểu của một DataMessage trong một GarlicClove trong một GarlicMessage, với overhead, vẫn là 128 byte. Một tùy chọn có thể cấu hình để tăng kích thước tối thiểu có thể được thêm vào trong tương lai.

- ID thông điệp thường được đặt thành một số ngẫu nhiên khi truyền và có vẻ bị bỏ qua khi nhận.

- Trong tương lai, certificate có thể được sử dụng cho HashCash để "trả phí" cho việc định tuyến.

### TunnelData {#msg-TunnelData}

#### Mô tả

Một tin nhắn được gửi từ cổng hoặc thành phần tham gia của một tunnel đến thành phần tham gia hoặc điểm cuối tiếp theo. Dữ liệu có độ dài cố định, chứa các tin nhắn I2NP bị phân mảnh, gom nhóm, thêm độn và mã hóa.

#### Mục lục

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Ghi chú

- ID thông điệp I2NP cho thông điệp này được đặt thành một số ngẫu nhiên mới tại mỗi hop.

- Xem thêm [Đặc tả Thông điệp Tunnel](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Mô tả

Gói một tin nhắn I2NP khác để gửi vào một tunnel tại cổng vào (inbound gateway) của tunnel đó.

#### Mục lục

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Ghi chú

- Payload là một thông điệp I2NP với header tiêu chuẩn 16-byte.

### Dữ liệu {#msg-Data}

#### Mô tả

Được sử dụng bởi Garlic Messages và Garlic Cloves để đóng gói dữ liệu tùy ý.

#### Mục lục

Một số nguyên độ dài, theo sau là dữ liệu không minh bạch.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Ghi chú

- Thông điệp này không chứa thông tin định tuyến và sẽ không bao giờ được gửi dưới dạng "unwrapped". Nó chỉ được sử dụng bên trong các thông điệp `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

ĐÃ LOẠI BỎ, hãy sử dụng [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Ghi chú

- Kể từ phiên bản 0.9.48, cũng có thể chứa ECIES-X25519 BuildRequestRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Xem thêm [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

- ID tin nhắn I2NP cho tin nhắn này phải được đặt theo đặc tả tạo tunnel.

- Mặc dù thông điệp này hiếm khi được thấy trong mạng ngày nay, đã được thay thế bởi thông điệp `VariableTunnelBuild`, nó vẫn có thể được sử dụng cho các tunnel rất dài và chưa bị loại bỏ. Các router phải triển khai.

### TunnelBuildReply {#msg-TunnelBuildReply}

ĐÃ LOẠI BỎ, hãy sử dụng [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Ghi chú

- Kể từ phiên bản 0.9.48, cũng có thể chứa ECIES-X25519 BuildResponseRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Xem thêm [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

- ID thông điệp I2NP cho thông điệp này phải được thiết lập theo đặc tả tạo tunnel.

- Mặc dù thông điệp này hiếm khi được thấy trong mạng ngày nay, đã được thay thế bởi thông điệp `VariableTunnelBuildReply`, nó vẫn có thể được sử dụng cho các tunnel rất dài và chưa bị loại bỏ. Router phải triển khai.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Ghi chú

- Kể từ phiên bản 0.9.48, cũng có thể chứa các ECIES-X25519 BuildRequestRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Thông điệp này được giới thiệu trong phiên bản router 0.7.12, và có thể không được gửi đến các tunnel participants có phiên bản cũ hơn.

- Xem thêm [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

- ID tin nhắn I2NP cho tin nhắn này phải được thiết lập theo đặc tả tạo tunnel.

- Số lượng bản ghi thông thường trong mạng hiện tại là 4, với tổng kích thước là 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Ghi chú

- Kể từ phiên bản 0.9.48, cũng có thể chứa ECIES-X25519 BuildResponseRecords, xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Thông điệp này được giới thiệu trong phiên bản router 0.7.12, và có thể không được gửi đến các tunnel participant có phiên bản cũ hơn.

- Xem thêm [đặc tả tạo tunnel](/docs/specs/tunnel-creation/).

- ID thông điệp I2NP cho thông điệp này phải được thiết lập theo đặc tả tạo tunnel.

- Số lượng bản ghi điển hình trong mạng hiện tại là 4, với tổng kích thước là 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Mô tả

Tính từ phiên bản API 0.9.51, chỉ dành cho các bộ định tuyến ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Ghi chú

- Kể từ phiên bản 0.9.51. Xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Thông báo này được giới thiệu trong phiên bản router 0.9.51, và có thể không được gửi đến các tunnel participants sớm hơn phiên bản đó.

- Số lượng bản ghi điển hình trong mạng hiện tại là 4, với tổng kích thước là 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Mô tả

Gửi từ điểm cuối đi của một đường hầm mới đến người khởi tạo. Dành riêng cho các bộ định tuyến ECIES-X25519, kể từ phiên bản API 0.9.51.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Ghi chú

- Từ phiên bản 0.9.51. Xem [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Số lượng bản ghi điển hình trong mạng ngày nay là 4, với tổng kích thước là 873.

## Tài liệu tham khảo

- **[CRYPTO-ELG]** [Cryptography - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Cấu trúc chung - Date](/docs/specs/common-structures/#date)
- **[ECIES]** [Đặc tả ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Đặc tả ECIES Routers](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Routing](/docs/overview/garlic-routing/)
- **[Hash]** [Cấu trúc chung - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [Giao thức I2NP](/docs/protocol/i2np/)
- **[Integer]** [Cấu trúc chung - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Đặc tả NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Đề xuất 156](/proposals/156/)
- **[Prop157]** [Đề xuất 157](/proposals/157/)
- **[RouterIdentity]** [Cấu trúc chung - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [Vận chuyển SSU](/docs/transports/ssu/)
- **[SSU-ED]** [Vận chuyển SSU - Thiết lập trực tiếp](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Đặc tả SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Hướng dẫn gửi thông điệp tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Đặc tả tạo tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Tạo tunnel ECIES](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Triển khai tunnel](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Đặc tả thông điệp tunnel](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Cấu trúc chung - TunnelId](/docs/specs/common-structures/#tunnelid)
