---
title: "Giao thức Client I2P (I2CP)"
description: "Cách các ứng dụng thương lượng phiên, tunnel và leaseSet với I2P router."
slug: "i2cp"
aliases:
  - "/vi/docs/api/i2cp"
  - "/vi/docs/api/i2cp/"
  - "/vi/docs/specs/i2cp-spec"
  - "/vi/docs/specs/i2cp-spec/"
  - "/vi/i2cp_spec"
  - "/vi/i2cp_spec/"
category: "Giao thức"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Tổng quan

Đây là đặc tả của I2P Control Protocol (I2CP), giao diện cấp thấp giữa các client và router. Các Java client sẽ sử dụng I2CP client API, cái mà triển khai giao thức này.

Không có triển khai non-Java nào được biết đến của thư viện client-side thực hiện I2CP. Thêm vào đó, các ứng dụng hướng socket (streaming) sẽ cần một triển khai của giao thức streaming, nhưng cũng không có thư viện non-Java nào cho việc đó. Do đó, các client non-Java thay vào đó nên sử dụng giao thức tầng cao hơn SAMv3 [SAMv3](/docs/api/samv3/), có các thư viện tồn tại trong nhiều ngôn ngữ.

Đây là một giao thức cấp thấp được hỗ trợ cả trong nội bộ và bên ngoài bởi Java I2P router. Giao thức chỉ được tuần tự hóa nếu client và router không nằm trong cùng một JVM; nếu không, các đối tượng Java của I2CP message sẽ được truyền qua giao diện JVM nội bộ. I2CP cũng được hỗ trợ bên ngoài bởi C++ router i2pd.

Thêm thông tin có thể tìm thấy trên trang Tổng quan I2CP [I2CP](/docs/specs/i2cp/).

## Phiên

Giao thức được thiết kế để xử lý nhiều "phiên", mỗi phiên có ID phiên 2 byte, qua một kết nối TCP duy nhất, tuy nhiên, nhiều phiên không được triển khai cho đến phiên bản 0.9.21. Xem [phần multisession bên dưới](#multisession). Không nên thử sử dụng nhiều phiên trên một kết nối I2CP duy nhất với các router cũ hơn phiên bản 0.9.21.

Có vẻ như cũng có một số điều khoản cho phép một client duy nhất nói chuyện với nhiều router qua các kết nối riêng biệt. Điều này cũng chưa được kiểm tra và có thể không hữu ích.

Không có cách nào để duy trì một session sau khi ngắt kết nối, hoặc khôi phục session đó trên một kết nối I2CP khác. Khi socket bị đóng, session sẽ bị hủy.

## Các Chuỗi Thông Điệp Mẫu

Lưu ý: Các ví dụ dưới đây không hiển thị Protocol Byte (0x2a) mà phải được gửi từ client đến router khi kết nối lần đầu. Thông tin chi tiết về khởi tạo kết nối có trên trang Tổng quan I2CP [I2CP](/docs/specs/i2cp/).

### Thiết lập Phiên Chuẩn

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Lấy Giới Hạn Băng Thông (Phiên Đơn Giản)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Tra cứu Đích đến (Phiên đơn giản)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Tin nhắn gửi đi

Phiên làm việc hiện tại, với i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Phiên hiện có, với i2cp.messageReliability=none và nonce khác không

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Phiên làm việc hiện có, với i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Tin nhắn đến

Phiên hiện tại, với i2cp.fastReceive=true (từ phiên bản 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Phiên làm việc hiện có, với i2cp.fastReceive=false (ĐÃ LỖI THỜI)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Ghi chú Đa phiên {#multisession}

Nhiều phiên trên một kết nối I2CP duy nhất được hỗ trợ kể từ phiên bản router 0.9.21. Phiên đầu tiên được tạo ra là "phiên chính". Các phiên bổ sung là "phiên phụ". Các phiên phụ được sử dụng để hỗ trợ nhiều đích đến chia sẻ một bộ tunnel chung. Ứng dụng ban đầu là để phiên chính sử dụng khóa ký ECDSA, trong khi phiên phụ sử dụng khóa ký DSA để giao tiếp với các eepsite cũ.

Các subsession chia sẻ cùng các tunnel pool đến và đi với phiên chính. Các subsession phải sử dụng cùng các khóa mã hóa với phiên chính. Điều này áp dụng cho cả khóa mã hóa LeaseSet và khóa mã hóa Destination (không sử dụng). Các subsession phải sử dụng các khóa ký khác nhau trong destination, do đó hash của destination sẽ khác với phiên chính. Vì các subsession sử dụng cùng khóa mã hóa và tunnel với phiên chính, mọi người đều có thể nhận ra rằng các Destination đang chạy trên cùng một router, vì vậy các đảm bảo ẩn danh chống tương quan thông thường không áp dụng.

Subsession được tạo bằng cách gửi thông điệp CreateSession và nhận thông điệp SessionStatus trả lời, như thường lệ. Subsession phải được tạo sau khi primary session đã được tạo. Phản hồi SessionStatus sẽ, khi thành công, chứa một Session ID duy nhất, khác biệt với ID của primary session. Mặc dù các thông điệp CreateSession nên được xử lý theo thứ tự, không có cách nào chắc chắn để liên kết một thông điệp CreateSession với phản hồi, vì vậy client không nên có nhiều thông điệp CreateSession đang chờ xử lý đồng thời. Các tùy chọn SessionConfig cho subsession có thể không được tuân thủ khi chúng khác với primary session. Đặc biệt, vì subsession sử dụng cùng tunnel pool với primary session, các tùy chọn tunnel có thể bị bỏ qua.

Router sẽ gửi các thông điệp RequestVariableLeaseSet riêng biệt cho mỗi Destination tới client, và client phải trả lời bằng thông điệp CreateLeaseSet cho mỗi thông điệp đó. Các lease cho hai Destination không nhất thiết phải giống hệt nhau, mặc dù chúng được chọn từ cùng một tunnel pool.

Một subsession có thể bị hủy bằng thông điệp DestroySession như thường lệ. Điều này sẽ không hủy session chính hoặc dừng kết nối I2CP. Tuy nhiên, việc hủy session chính sẽ hủy tất cả các subsession và dừng kết nối I2CP. Một thông điệp Disconnect sẽ hủy tất cả các session.

Lưu ý rằng hầu hết, nhưng không phải tất cả, các thông điệp I2CP đều chứa Session ID. Đối với những thông điệp không chứa Session ID, client có thể cần logic bổ sung để xử lý đúng cách các phản hồi từ router. DestLookup và DestReply không chứa Session ID; thay vào đó hãy sử dụng HostLookup và HostReply mới hơn. GetBandwidthLimts và BandwidthLimits không chứa session ID, tuy nhiên phản hồi không phụ thuộc vào session cụ thể.

### Ghi chú phiên bản {#notes}

Byte phiên bản giao thức ban đầu (0x2a) được gửi bởi client dự kiến sẽ không thay đổi. Trước phiên bản 0.8.7, thông tin phiên bản của router không có sẵn cho client, do đó ngăn cản các client mới hoạt động với các router cũ. Kể từ phiên bản 0.8.7, chuỗi phiên bản giao thức của hai bên được trao đổi trong Get/Set Date Messages. Tiếp tục, các client có thể sử dụng thông tin này để giao tiếp chính xác với các router cũ. Các client và router không nên gửi các thông điệp không được hỗ trợ bởi bên kia, vì chúng thường ngắt kết nối phiên làm việc khi nhận được thông điệp không được hỗ trợ.

Thông tin phiên bản được trao đổi là phiên bản API "cốt lõi" hoặc phiên bản giao thức I2CP, và không nhất thiết phải là phiên bản router.

Một tóm tắt cơ bản về các phiên bản giao thức I2CP như sau. Để biết chi tiết, hãy xem bên dưới.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Các cấu trúc phổ biến {#structures}

### Header thông điệp I2CP {#struct-I2CPMessageHeader}

#### Mô tả

Header chung cho tất cả các thông điệp I2CP, chứa độ dài thông điệp và loại thông điệp.

#### Nội dung

1.  4 byte [Integer](/docs/specs/common-structures/#integer) chỉ định độ dài của
    thân thông điệp
2.  1 byte [Integer](/docs/specs/common-structures/#integer) chỉ định loại thông điệp.
3.  Thân thông điệp I2CP, 0 hoặc nhiều byte hơn

#### Ghi chú

Giới hạn độ dài thông điệp thực tế là khoảng 64 KB.

### ID Tin nhắn {#struct-MessageId}

#### Mô tả

Xác định duy nhất một thông điệp đang chờ trên một router cụ thể tại một thời điểm. Điều này luôn được tạo ra bởi router và KHÔNG giống với nonce được tạo ra bởi client.

#### Mục lục

1.  4 byte [Integer](/docs/specs/common-structures/#integer)

#### Ghi chú

Message ID chỉ duy nhất trong một phiên làm việc; chúng không duy nhất trên toàn cục.

### Payload {#struct-Payload}

#### Mô tả

Cấu trúc này là nội dung của một thông điệp được gửi từ Destination này đến Destination khác.

#### Nội dung

1.  4 byte [Integer](/docs/specs/common-structures/#integer) độ dài
2.  Nhiều byte đó

#### Ghi chú

Payload ở định dạng gzip như được chỉ định trong trang Tổng quan I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

Giới hạn độ dài thông điệp thực tế là khoảng 64 KB.

### Session Config {#struct-SessionConfig}

#### Mô tả

Định nghĩa các tùy chọn cấu hình cho một phiên client cụ thể.

#### Nội dung

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) các tùy chọn
3.  [Date](/docs/specs/common-structures/#date) tạo
4.  [Signature](/docs/specs/common-structures/#signature) của 3 trường trước đó,
    được ký bởi [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Ghi chú

- Các tùy chọn được chỉ định trên trang Tổng quan I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- [Mapping](/docs/specs/common-structures/#mapping) phải được sắp xếp theo key để
  chữ ký được xác thực chính xác trong router.
- Ngày tạo phải nằm trong khoảng +/- 30 giây so với thời gian hiện tại
  khi được xử lý bởi router, nếu không config sẽ bị từ chối.

#### Chữ ký ngoại tuyến

- Nếu [Destination](/docs/specs/common-structures/#destination) được ký ngoại tuyến,
  [Mapping](/docs/specs/common-structures/#mapping) phải chứa ba tùy chọn
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, và
  i2cp.leaseSetOfflineSignature. 
  [Signature](/docs/specs/common-structures/#signature) sau đó được tạo bởi
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) tạm thời và
  được xác minh với
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) được chỉ định trong
  i2cp.leaseSetTransientPublicKey. Xem
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) để biết chi tiết.

### ID phiên {#struct-SessionId}

#### Mô tả

Xác định duy nhất một phiên làm việc trên một router cụ thể tại một thời điểm.

#### Mục lục

1.  2 byte [Integer](/docs/specs/common-structures/#integer)

#### Ghi chú

Session ID 0xffff được sử dụng để biểu thị "không có session", ví dụ như cho việc tra cứu hostname.

## Tin nhắn

Xem thêm [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Các Loại Thông Điệp {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Mô tả

Thông báo cho client về giới hạn băng thông.

Được gửi từ Router đến Client để phản hồi cho [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Nội dung

1.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn inbound của Client
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn outbound của Client
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn inbound của router
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn burst inbound của router
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn outbound của router
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Giới hạn burst outbound của router
    (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Thời gian burst của router
    (giây)
8.  Chín [Integer](/docs/specs/common-structures/#integer) 4-byte (không xác định)

#### Ghi chú

Giới hạn client có thể là những giá trị duy nhất được thiết lập, và có thể là giới hạn thực tế của router, hoặc một phần trăm của giới hạn router, hoặc cụ thể cho client riêng biệt đó, tùy thuộc vào cách triển khai. Tất cả các giá trị được gắn nhãn là giới hạn router có thể bằng 0, tùy thuộc vào cách triển khai. Tính từ bản phát hành 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Mô tả

Thông báo cho router biết rằng một Destination đang bị làm mờ (blinded), với mật khẩu tra cứu tùy chọn và khóa riêng tùy chọn để giải mã. Xem đề xuất 123 và 149 để biết chi tiết.

Router cần biết liệu một đích đến có được che dấu (blinded) hay không. Nếu nó được che dấu và sử dụng xác thực bí mật hoặc xác thực theo từng client, router cũng cần có thông tin đó.

Một Host Lookup của địa chỉ b32 định dạng mới ("b33") cho router biết rằng địa chỉ đó được làm mờ, nhưng không có cơ chế nào để truyền khóa bí mật hoặc khóa riêng tư cho router trong thông điệp Host Lookup. Mặc dù chúng ta có thể mở rộng thông điệp Host Lookup để thêm thông tin đó, nhưng sẽ gọn gàng hơn nếu định nghĩa một thông điệp mới.

Thông báo này cung cấp một cách lập trình để client thông báo với router. Nếu không, người dùng sẽ phải cấu hình thủ công từng destination.

#### Cách sử dụng

Trước khi một client gửi tin nhắn đến một điểm đến được làm mù (blinded destination), nó phải tra cứu "b33" trong tin nhắn Host Lookup, hoặc gửi tin nhắn Blinding Info. Nếu điểm đến được làm mù yêu cầu mật khẩu bí mật hoặc xác thực theo từng client, client phải gửi tin nhắn Blinding Info.

Router không gửi phản hồi cho thông điệp này. Được gửi từ Client đến Router.

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Thứ tự bit: 76543210 > - Bit 0: 0 cho mọi người, 1 cho từng client > - Bit 3-1: Lược đồ xác thực, nếu bit 0 được đặt thành 1 cho >   từng client, ngược lại 000 >   - 000: Xác thực client DH (hoặc không có xác thực từng client) >   - 001: Xác thực client PSK > - Bit 4: 1 nếu yêu cầu bí mật, 0 nếu không yêu cầu bí mật > - Bit 7-5: Không sử dụng, đặt thành 0 để tương thích trong tương lai

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Loại endpoint

> - Type 0 là một [Hash](/docs/specs/common-structures/#hash) > - Type 1 là một hostname [String](/docs/specs/common-structures/#string) > - Type 2 là một [Destination](/docs/specs/common-structures/#destination) > - Type 3 là một Sig Type và >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Expiration Seconds kể từ
    epoch
6.  Endpoint: Dữ liệu như được chỉ định, một trong số

> - Loại 0: 32 byte [Hash](/docs/specs/common-structures/#hash) > > - Loại 1: tên host [String](/docs/specs/common-structures/#string) > > - Loại 2: nhị phân [Destination](/docs/specs/common-structures/#destination) > >  > >  - Loại 3: 2 byte [Integer](/docs/specs/common-structures/#integer) loại chữ ký, theo sau là > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (độ dài như >       được ngụ ý bởi loại chữ ký)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Khóa giải mã Chỉ có mặt
    nếu flag bit 0 được đặt thành 1. Một khóa riêng ECIES_X25519 32-byte,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Mật khẩu tra cứu Chỉ có mặt nếu
    flag bit 4 được đặt thành 1.

#### Ghi chú

- Tính đến phiên bản 0.9.43.
- Kiểu endpoint Hash có lẽ không hữu ích trừ khi router có thể thực hiện
  tra cứu ngược trong sổ địa chỉ để lấy Destination.
- Kiểu endpoint hostname có lẽ không hữu ích trừ khi router
  có thể thực hiện tra cứu trong sổ địa chỉ để lấy Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

ĐÃ NGỪNG SỬ DỤNG. Không thể sử dụng cho LeaseSet2, offline keys, các kiểu mã hóa không phải ElGamal, nhiều kiểu mã hóa, hoặc LeaseSets được mã hóa. Sử dụng CreateLeaseSet2Message với tất cả routers phiên bản 0.9.39 trở lên.

#### Mô tả

Thông điệp này được gửi để phản hồi một [RequestLeaseSetMessage](#RequestLeaseSetMessage) hoặc [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) và chứa tất cả các cấu trúc [Lease](/docs/specs/common-structures/#lease) cần được xuất bản lên I2NP Network Database.

Gửi từ Client đến Router.

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) hoặc 20
    byte được bỏ qua
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Ghi chú

SigningPrivateKey khớp với [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) từ trong LeaseSet, chỉ khi loại signing key là DSA. Điều này dành cho việc thu hồi LeaseSet, tính năng chưa được triển khai và không có khả năng sẽ được triển khai. Nếu loại signing key không phải là DSA, trường này chứa 20 byte dữ liệu ngẫu nhiên. Độ dài của trường này luôn là 20 byte, nó không bao giờ bằng độ dài của signing private key không phải DSA.

PrivateKey phù hợp với [PublicKey](/docs/specs/common-structures/#publickey) từ LeaseSet. PrivateKey là cần thiết để giải mã các thông điệp được định tuyến garlic.

Việc thu hồi chưa được triển khai. Kết nối đến nhiều router chưa được triển khai trong bất kỳ thư viện client nào.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Mô tả

Thông điệp này được gửi để phản hồi một [RequestLeaseSetMessage](#RequestLeaseSetMessage) hoặc [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) và chứa tất cả các cấu trúc [Lease](/docs/specs/common-structures/#lease) cần được công bố lên I2NP Network Database.

Gửi từ Client đến Router. Kể từ phiên bản 0.9.39. Xác thực theo từng client cho EncryptedLeaseSet được hỗ trợ từ phiên bản 0.9.41. MetaLeaseSet chưa được hỗ trợ qua I2CP. Xem đề xuất 123 để biết thêm thông tin.

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  Một byte loại lease set theo sau.

> - Type 1 là một [LeaseSet](/docs/specs/common-structures/#leaseset) (đã lỗi thời) > - Type 3 là một [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Type 5 là một [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Type 7 là một [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) hoặc
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) hoặc
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) hoặc
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Một byte chỉ số lượng khóa riêng tư theo sau.
5.  Danh sách [PrivateKey](/docs/specs/common-structures/#privatekey). Một khóa cho mỗi khóa
    công khai trong leaseSet, theo cùng thứ tự. (Không có mặt đối với Meta LS2)

> - Loại mã hóa (2 byte [Integer](/docs/specs/common-structures/#integer)) > - Độ dài khóa mã hóa (2 byte [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) mã hóa (số byte >   được chỉ định)

#### Ghi chú

Các PrivateKeys khớp với từng [PublicKey](/docs/specs/common-structures/#publickey) từ LeaseSet. Các PrivateKeys cần thiết để giải mã các thông điệp được định tuyến garlic.

Xem đề xuất 123 để biết thêm thông tin về Encrypted LeaseSets.

Nội dung và định dạng cho MetaLeaseSet đang trong giai đoạn sơ bộ và có thể thay đổi. Không có giao thức cụ thể nào được chỉ định để quản lý nhiều router. Xem đề xuất 123 để biết thêm thông tin.

Khóa riêng tư ký, trước đây được định nghĩa cho việc thu hồi và không được sử dụng, không có mặt trong LS2.

Phiên bản sơ bộ với loại thông điệp 40 đã có trong 0.9.38 nhưng định dạng đã được thay đổi. Loại 40 đã bị loại bỏ và không được hỗ trợ. Loại 41 không hợp lệ cho đến 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Mô tả

Thông điệp này được gửi từ client để khởi tạo một session, trong đó session được định nghĩa là kết nối của một Destination duy nhất tới mạng, qua đó tất cả các thông điệp dành cho Destination đó sẽ được chuyển đến và từ đó tất cả các thông điệp mà Destination đó gửi đến bất kỳ Destination nào khác sẽ được gửi đi.

Gửi từ Client đến Router. Router phản hồi bằng một [SessionStatusMessage](#SessionStatusMessage).

#### Mục lục

1.  [Cấu hình phiên](#struct-sessionconfig)

#### Ghi chú

- Đây là thông điệp thứ hai được gửi bởi client. Trước đó client đã
  gửi một [GetDateMessage](#GetDateMessage) và nhận được phản hồi
  [SetDateMessage](#SetDateMessage).
- Nếu Date trong Session Config quá xa (hơn +/- 30
  giây) so với thời gian hiện tại của router, session sẽ bị
  từ chối.
- Nếu đã có một session trên router cho Destination này, 
  session sẽ bị từ chối.
- [Mapping](/docs/specs/common-structures/#mapping) trong Session Config phải được
  sắp xếp theo key để signature sẽ được xác thực chính xác trong
  router.

### DestLookupMessage {#DestLookupMessage}

#### Mô tả

Được gửi từ Client đến Router. Router phản hồi bằng một [DestReplyMessage](#DestReplyMessage).

#### Mục lục

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Ghi chú

Kể từ phiên bản phát hành 0.7.

Kể từ phiên bản 0.8.3, nhiều tra cứu đồng thời được hỗ trợ, và tra cứu được hỗ trợ trong cả I2PSimpleSession và các phiên làm việc tiêu chuẩn.

[HostLookupMessage](#HostLookupMessage) được ưu tiên sử dụng kể từ phiên bản 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Mô tả

Được gửi từ Router đến Client để phản hồi một [DestLookupMessage](#DestLookupMessage).

#### Nội dung

1.  [Destination](/docs/specs/common-structures/#destination) khi thành công, hoặc
    [Hash](/docs/specs/common-structures/#hash) khi thất bại

#### Ghi chú

Kể từ phiên bản 0.7.

Kể từ phiên bản 0.8.3, Hash được yêu cầu sẽ được trả về nếu việc tra cứu thất bại, để client có thể có nhiều tra cứu đồng thời và liên kết các phản hồi với các tra cứu. Để liên kết phản hồi Destination với yêu cầu, hãy lấy Hash của Destination. Trước phiên bản 0.8.3, phản hồi sẽ trống nếu thất bại.

### DestroySessionMessage {#DestroySessionMessage}

#### Mô tả

Thông điệp này được gửi từ client để hủy một phiên làm việc.

Được gửi từ Client đến Router. Router sẽ phản hồi bằng một [SessionStatusMessage](#SessionStatusMessage) (Destroyed). Tuy nhiên, hãy xem các lưu ý quan trọng bên dưới.

#### Nội dung

1.  [ID Phiên](#struct-sessionid)

#### Ghi chú

Router tại thời điểm này nên giải phóng tất cả các tài nguyên liên quan đến phiên làm việc.

Thông qua API 0.9.66, router I2P Java và các thư viện client khác biệt đáng kể so với đặc tả này. Router không bao giờ gửi phản hồi SessionStatus(Destroyed). Nếu không còn session nào, nó sẽ gửi [DisconnectMessage](#DisconnectMessage). Nếu có các subsession hoặc session chính vẫn còn, nó không trả lời.

Thư viện client Java phản hồi với thông điệp SessionStatus bằng cách hủy tất cả các phiên và kết nối lại.

Việc hủy các subsession riêng lẻ trên một kết nối có nhiều session có thể chưa được kiểm tra đầy đủ hoặc chưa hoạt động trên các triển khai router và client khác nhau. Hãy thận trọng khi sử dụng.

Các triển khai nên xem việc hủy một phiên chính như là hủy tất cả các phiên phụ, nhưng cho phép hủy một phiên phụ đơn lẻ và giữ kết nối mở, tuy nhiên Java I2P hiện tại không làm như vậy. Nếu hành vi của Java I2P được thay đổi trong các phiên bản tiếp theo, nó sẽ được ghi lại tại đây.

### DisconnectMessage {#DisconnectMessage}

#### Mô tả

Thông báo cho bên kia rằng có vấn đề và kết nối hiện tại sắp bị hủy. Điều này kết thúc tất cả các phiên trên kết nối đó. Socket sẽ được đóng trong thời gian ngắn. Được gửi từ router tới client hoặc từ client tới router.

#### Mục lục

1.  Lý do [String](/docs/specs/common-structures/#string)

#### Ghi chú

Chỉ được triển khai theo hướng từ router đến client, ít nhất là trong Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Mô tả

Yêu cầu router thông báo giới hạn băng thông hiện tại của nó.

Được gửi từ Client đến Router. Router phản hồi bằng một [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Mục lục

*Không có*

#### Ghi chú

Từ phiên bản phát hành 0.7.2.

Kể từ phiên bản 0.8.3, được hỗ trợ trong cả I2PSimpleSession và các phiên làm việc tiêu chuẩn.

### GetDateMessage {#GetDateMessage}

#### Mô tả

Gửi từ Client đến Router. Router phản hồi với một [SetDateMessage](#SetDateMessage).

#### Mục lục

1.  Phiên bản I2CP API [String](/docs/specs/common-structures/#string)
2.  Xác thực [Mapping](/docs/specs/common-structures/#mapping) (tùy chọn, kể từ
    phiên bản 0.9.11)

#### Ghi chú

- Thông thường là thông điệp đầu tiên được gửi bởi client sau khi gửi
  byte phiên bản giao thức.
- Chuỗi phiên bản được bao gồm từ bản phát hành 0.8.7. Điều này chỉ
  hữu ích nếu client và router không ở trong cùng một JVM. Nếu nó không
  có mặt, client là phiên bản 0.8.6 hoặc cũ hơn.
- Từ bản phát hành 0.9.11, xác thực
  [Mapping](/docs/specs/common-structures/#mapping) có thể được bao gồm, với các khóa
  i2cp.username và i2cp.password. Mapping không cần được sắp xếp vì
  thông điệp này không được ký. Trước và bao gồm 0.9.10,
  xác thực được bao gồm trong
  [Session Config](#struct-sessionconfig)
  Mapping, và không có xác thực nào được thực thi cho
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), hoặc
  [DestLookupMessage](#DestLookupMessage). Khi được kích hoạt, xác thực
  thông qua [GetDateMessage](#GetDateMessage) được yêu cầu trước bất kỳ thông điệp nào khác
  từ bản phát hành 0.9.16. Điều này chỉ hữu ích bên ngoài ngữ cảnh
  router. Đây là một thay đổi không tương thích, nhưng sẽ chỉ ảnh hưởng đến các phiên
  bên ngoài ngữ cảnh router với xác thực, điều này nên hiếm.

### HostLookupMessage {#HostLookupMessage}

#### Mô tả

Được gửi từ Client đến Router. Router sẽ phản hồi bằng một [HostReplyMessage](#HostReplyMessage).

Điều này thay thế [DestLookupMessage](#DestLookupMessage) và thêm ID yêu cầu, thời gian chờ, và hỗ trợ tra cứu tên máy chủ. Vì nó cũng hỗ trợ tra cứu Hash, nó có thể được sử dụng cho tất cả các tra cứu nếu router hỗ trợ. Đối với tra cứu tên máy chủ, router sẽ truy vấn dịch vụ đặt tên của ngữ cảnh của nó. Điều này chỉ hữu ích nếu client nằm bên ngoài ngữ cảnh của router. Bên trong ngữ cảnh router, client nên truy vấn dịch vụ đặt tên trực tiếp, điều này hiệu quả hơn nhiều.

#### Nội dung

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) request ID
3.  4 byte [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) loại request
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) hoặc tên host
    [String](/docs/specs/common-structures/#string) hoặc
    [Destination](/docs/specs/common-structures/#destination)

Các loại yêu cầu:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Loại 2-4 yêu cầu ánh xạ tùy chọn từ LeaseSet được trả về trong thông điệp HostReply. Xem đề xuất 167.

#### Ghi chú

- Kể từ phiên bản 0.9.11. Sử dụng [DestLookupMessage](#DestLookupMessage) cho
  các router cũ hơn.
- Session ID và request ID sẽ được trả về trong
  [HostReplyMessage](#HostReplyMessage). Sử dụng 0xFFFF cho session ID
  nếu không có session.
- Timeout hữu ích cho việc tra cứu Hash. Khuyến nghị tối thiểu 10,000 (10
  giây). Trong tương lai nó cũng có thể hữu ích cho việc tra cứu dịch vụ
  đặt tên từ xa. Giá trị này có thể không được tôn trọng đối với việc tra cứu
  tên host cục bộ, vốn nên nhanh chóng.
- Tra cứu tên host Base 32 được hỗ trợ nhưng tốt hơn là chuyển đổi
  thành Hash trước.

### HostReplyMessage {#HostReplyMessage}

#### Mô tả

Được gửi từ Router đến Client để phản hồi [HostLookupMessage](#HostLookupMessage).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) ID yêu cầu
3.  1 byte [Integer](/docs/specs/common-structures/#integer) mã kết quả

> - 0: Thành công > - 1: Thất bại > - 2: Yêu cầu mật khẩu tra cứu (từ phiên bản 0.9.43) > - 3: Yêu cầu khóa riêng (từ phiên bản 0.9.43) > - 4: Yêu cầu mật khẩu tra cứu và khóa riêng (từ phiên bản 0.9.43) > - 5: Lỗi giải mã leaseSet (từ phiên bản 0.9.43) > - 6: Lỗi tra cứu leaseSet (từ phiên bản 0.9.66) > - 7: Loại tra cứu không được hỗ trợ (từ phiên bản 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), chỉ có mặt nếu mã kết quả
    là zero, ngoại trừ cũng có thể được trả về cho các loại lookup 2-4. Xem
    bên dưới.
5.  [Mapping](/docs/specs/common-structures/#mapping), chỉ có mặt nếu mã kết quả là
    zero, chỉ được trả về cho các loại lookup 2-4. Kể từ 0.9.66. Xem bên dưới.

#### Phản hồi cho các loại lookup 2-4

Proposal 167 định nghĩa các loại tra cứu bổ sung trả về tất cả các tùy chọn từ leaseset, nếu có. Đối với các loại tra cứu 2-4, router phải lấy leaseset, ngay cả khi khóa tra cứu có trong sổ địa chỉ.

Nếu thành công, HostReply sẽ chứa Mapping các tùy chọn từ leaseset, và bao gồm nó như mục 5 sau destination. Nếu không có tùy chọn nào trong Mapping, hoặc leaseset là phiên bản 1, nó vẫn sẽ được bao gồm như một Mapping rỗng (hai byte: 0 0). Tất cả các tùy chọn từ leaseset sẽ được bao gồm, không chỉ các tùy chọn service record. Ví dụ, các tùy chọn cho các tham số được định nghĩa trong tương lai có thể có mặt. Mapping được trả về có thể được sắp xếp hoặc không, tùy thuộc vào cách triển khai.

Khi tra cứu leaseset thất bại, phản hồi sẽ chứa mã lỗi mới là 6 (Leaseset lookup failure) và sẽ không bao gồm ánh xạ. Khi mã lỗi 6 được trả về, trường Destination có thể có hoặc không có mặt. Nó sẽ có mặt nếu việc tra cứu tên máy chủ trong sổ địa chỉ thành công, hoặc nếu một lần tra cứu trước đó thành công và kết quả đã được lưu trong bộ nhớ đệm, hoặc nếu Destination có mặt trong thông điệp tra cứu (loại tra cứu 4).

Nếu một kiểu lookup không được hỗ trợ, phản hồi sẽ chứa mã lỗi mới 7 (kiểu lookup không được hỗ trợ).

#### Ghi chú

- Kể từ phiên bản 0.9.11. Xem ghi chú [HostLookupMessage](#HostLookupMessage).
- Session ID và request ID là những ID từ [HostLookupMessage](#HostLookupMessage).
- Mã kết quả là 0 cho thành công, 1-255 cho thất bại. 1 biểu thị lỗi chung. Kể từ 0.9.43, các mã lỗi bổ sung 2-5 đã được định nghĩa để hỗ trợ lỗi mở rộng cho tra cứu "b33". Xem đề xuất 123 và 149 để biết thêm thông tin. Kể từ 0.9.66, các mã lỗi bổ sung 6-7 đã được định nghĩa để hỗ trợ lỗi mở rộng cho tra cứu loại 2-4. Xem đề xuất 167 để biết thêm thông tin.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Mô tả

Gửi tải trọng của một thông điệp đến client.

Được gửi từ Router tới Client. Nếu i2cp.fastReceive=true, điều này không phải là mặc định, client sẽ phản hồi bằng một [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Mục lục

1.  [ID Phiên](#struct-sessionid)
2.  [ID Tin nhắn](#struct-messageid)
3.  [Payload](#struct-payload)

#### Ghi chú

### MessageStatusMessage {#MessageStatusMessage}

#### Mô tả

Thông báo cho client về trạng thái giao hàng của một tin nhắn đến hoặc đi. Được gửi từ Router đến Client. Nếu tin nhắn này cho biết rằng có một tin nhắn đến có sẵn, client sẽ phản hồi bằng một [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Đối với tin nhắn đi, đây là phản hồi cho một [SendMessageMessage](#SendMessageMessage) hoặc [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) được tạo bởi router
3.  1 byte [Integer](/docs/specs/common-structures/#integer) trạng thái
4.  4 byte [Integer](/docs/specs/common-structures/#integer) kích thước
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce được tạo trước đó
    bởi client

#### Ghi chú

Thông qua phiên bản 0.9.4, các giá trị trạng thái đã biết là 0 cho thông báo có sẵn, 1 cho đã chấp nhận, 2 cho best effort thành công, 3 cho best effort thất bại, 4 cho guaranteed thành công, 5 cho guaranteed thất bại. Integer kích thước chỉ định kích thước của thông báo có sẵn và chỉ có liên quan khi status = 0. Mặc dù guaranteed chưa được triển khai (best effort là dịch vụ duy nhất), việc triển khai router hiện tại sử dụng các mã trạng thái guaranteed, không phải mã best effort.

Kể từ phiên bản router 0.9.5, các mã trạng thái bổ sung đã được định nghĩa, tuy nhiên chúng không nhất thiết được triển khai. Xem [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) để biết chi tiết. Đối với các tin nhắn gửi đi, các mã 1, 2, 4, và 6 cho biết thành công; tất cả các mã khác đều là lỗi. Các mã lỗi trả về có thể khác nhau và phụ thuộc vào cách triển khai.

Tất cả mã trạng thái:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Khi status = 1 (được chấp nhận), nonce sẽ khớp với nonce trong [SendMessageMessage](#SendMessageMessage), và Message ID được bao gồm sẽ được sử dụng cho thông báo thành công hoặc thất bại tiếp theo. Ngược lại, nonce có thể bị bỏ qua.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

ĐÃ LỖI THỜI. Không được hỗ trợ bởi i2pd.

#### Mô tả

Yêu cầu router gửi một thông điệp mà nó đã được thông báo trước đó. Được gửi từ Client đến Router. Router sẽ phản hồi bằng một [MessagePayloadMessage](#MessagePayloadMessage).

#### Mục lục

1.  [ID Phiên](#struct-sessionid)
2.  [ID Tin nhắn](#struct-messageid)

#### Ghi chú

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) được gửi như một phản hồi cho [MessageStatusMessage](#MessageStatusMessage) thông báo rằng có một tin nhắn mới sẵn sàng để nhận. Nếu message id được chỉ định trong [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) không hợp lệ hoặc không chính xác, router có thể đơn giản không phản hồi, hoặc có thể gửi lại một [DisconnectMessage](#DisconnectMessage).

Điều này không được sử dụng trong chế độ "fast receive" (nhận nhanh), đây là chế độ mặc định kể từ phiên bản 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

ĐÃ LỖI THỜI. Không được hỗ trợ bởi i2pd.

#### Mô tả

Thông báo cho router rằng việc giao hàng tin nhắn đã hoàn thành thành công và router có thể loại bỏ tin nhắn đó.

Được gửi từ Client đến Router.

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid)

#### Ghi chú

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage) được gửi sau khi [MessagePayloadMessage](#MessagePayloadMessage) đã chuyển phát đầy đủ payload của một thông điệp.

Điều này không được sử dụng trong chế độ "fast receive" (nhận nhanh), đây là chế độ mặc định kể từ phiên bản 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Mô tả

Được gửi từ Client đến Router để cập nhật cấu hình phiên. Router sẽ phản hồi bằng một [SessionStatusMessage](#SessionStatusMessage).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  [Cấu hình Session](#struct-sessionconfig)

#### Ghi chú

- Kể từ phiên bản 0.7.1.
- Nếu Date trong Session Config quá xa (hơn +/- 30
  giây) so với thời gian hiện tại của router, session sẽ bị
  từ chối.
- [Mapping](/docs/specs/common-structures/#mapping) trong Session Config phải được
  sắp xếp theo key để chữ ký được xác thực đúng cách trong
  router.
- Một số tùy chọn cấu hình chỉ có thể được thiết lập trong
  [CreateSessionMessage](#CreateSessionMessage), và các thay đổi ở đây sẽ
  không được router nhận ra. Các thay đổi đối với tùy chọn tunnel inbound.\*
  và outbound.\* luôn được nhận ra.
- Nói chung, router nên hợp nhất config đã cập nhật với
  config hiện tại, vì vậy config đã cập nhật chỉ cần chứa các tùy chọn mới hoặc
  đã thay đổi. Tuy nhiên, do việc hợp nhất, các tùy chọn có thể không được
  loại bỏ theo cách này; chúng phải được thiết lập rõ ràng về giá trị
  mặc định mong muốn.

### ReportAbuseMessage {#ReportAbuseMessage}

ĐÃ LỖI THỜI, KHÔNG SỬ DỤNG, KHÔNG HỖ TRỢ

#### Mô tả

Thông báo cho bên kia (client hoặc router) rằng họ đang bị tấn công, có thể kèm theo tham chiếu đến một MessageId cụ thể. Nếu router đang bị tấn công, client có thể quyết định chuyển sang router khác, và nếu client đang bị tấn công, router có thể xây dựng lại các router của mình hoặc đưa vào danh sách cấm một số peer đã gửi tin nhắn thực hiện cuộc tấn công.

Được gửi từ router tới client hoặc từ client tới router.

#### Nội dung

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) mức độ lạm dụng (0 là ít lạm dụng nhất, 255 là cực kỳ lạm dụng)
3.  Lý do [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Ghi chú

Không được sử dụng. Chưa được triển khai đầy đủ. Cả router và client đều có thể tạo ra [ReportAbuseMessage](#ReportAbuseMessage), nhưng không có bộ xử lý nào cho thông điệp này khi được nhận.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

ĐÃ KHÔNG CÒN HỖ TRỢ. Không được i2pd hỗ trợ. Không được Java I2P gửi đến các client phiên bản 0.9.7 trở lên (2013-07). Sử dụng RequestVariableLeaseSetMessage.

#### Mô tả

Yêu cầu một client ủy quyền việc bao gồm một tập hợp cụ thể các tunnel đến. Được gửi từ Router đến Client. Client sẽ phản hồi bằng một [CreateLeaseSetMessage](#CreateLeaseSetMessage).

Thông điệp đầu tiên được gửi trên một phiên là tín hiệu cho client biết rằng các tunnel đã được xây dựng và sẵn sàng cho lưu lượng. Router không được gửi thông điệp đầu tiên này cho đến khi ít nhất một tunnel đến VÀ một tunnel đi đã được xây dựng. Các client nên timeout và hủy phiên nếu thông điệp đầu tiên này không được nhận sau một khoảng thời gian (khuyến nghị: 5 phút hoặc hơn).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) số lượng tunnel
3.  Nhiều cặp như vậy:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  [Date](/docs/specs/common-structures/#date) kết thúc

#### Ghi chú

Điều này yêu cầu một [LeaseSet](/docs/specs/common-structures/#leaseset) với tất cả các mục [Lease](/docs/specs/common-structures/#lease) được thiết lập hết hạn cùng một lúc. Đối với các phiên bản client 0.9.7 hoặc cao hơn, [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) được sử dụng.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Mô tả

Yêu cầu client ủy quyền cho việc bao gồm một tập hợp cụ thể các tunnel đến.

Gửi từ Router đến Client. Client phản hồi bằng [CreateLeaseSetMessage](#CreateLeaseSetMessage) hoặc [CreateLeaseSet2Message](#CreateLeaseSet2Message).

Thông báo đầu tiên được gửi trong một phiên là tín hiệu cho client biết rằng các tunnel đã được xây dựng và sẵn sàng cho lưu lượng. Router không được gửi thông báo đầu tiên này cho đến khi ít nhất một tunnel đến VÀ một tunnel đi đã được xây dựng. Các client nên timeout và hủy phiên nếu không nhận được thông báo đầu tiên này sau một khoảng thời gian (khuyến nghị: 5 phút hoặc hơn).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) số lượng tunnel
3.  Nhiều bằng số đó các mục [Lease](/docs/specs/common-structures/#lease)

#### Ghi chú

Yêu cầu này lấy một [LeaseSet](/docs/specs/common-structures/#leaseset) với thời gian hết hạn riêng biệt cho từng [Lease](/docs/specs/common-structures/#lease).

Kể từ phiên bản 0.9.7. Đối với các client trước phiên bản đó, hãy sử dụng [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Mô tả

Đây là cách một client gửi tin nhắn (payload) đến [Destination](/docs/specs/common-structures/#destination). Router sẽ sử dụng thời gian hết hạn mặc định.

Gửi từ Client đến Router. Router phản hồi bằng một [MessageStatusMessage](#MessageStatusMessage).

#### Mục lục

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce

#### Ghi chú

Ngay khi [SendMessageMessage](#SendMessageMessage) đến đầy đủ và nguyên vẹn, router sẽ trả về một [MessageStatusMessage](#MessageStatusMessage) thông báo rằng thông điệp đã được chấp nhận để gửi đi. Thông điệp đó sẽ chứa cùng nonce được gửi ở đây. Sau đó, dựa trên các đảm bảo gửi của cấu hình phiên, router có thể gửi thêm một [MessageStatusMessage](#MessageStatusMessage) khác để cập nhật trạng thái.

Kể từ phiên bản 0.8.1, router không gửi [MessageStatusMessage](#MessageStatusMessage) nào nếu i2cp.messageReliability=none.

Trước phiên bản 0.9.4, giá trị nonce bằng 0 không được phép. Từ phiên bản 0.9.4 trở đi, giá trị nonce bằng 0 được cho phép và thông báo cho router rằng nó không nên gửi [MessageStatusMessage](#MessageStatusMessage), tức là nó hoạt động như thể i2cp.messageReliability=none chỉ cho thông điệp này.

Trước phiên bản 0.9.14, một phiên với i2cp.messageReliability=none không thể được ghi đè trên cơ sở từng tin nhắn. Kể từ phiên bản 0.9.14, trong một phiên với i2cp.messageReliability=none, client có thể yêu cầu gửi một [MessageStatusMessage](#MessageStatusMessage) với thông báo thành công hoặc thất bại của việc gửi bằng cách đặt nonce thành một giá trị khác không. Router sẽ không gửi [MessageStatusMessage](#MessageStatusMessage) "đã chấp nhận" nhưng sau đó sẽ gửi cho client một [MessageStatusMessage](#MessageStatusMessage) với cùng nonce, và một giá trị thành công hoặc thất bại.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Mô tả

Gửi từ Client đến Router. Giống như [SendMessageMessage](#SendMessageMessage), ngoại trừ bao gồm thời gian hết hạn và các tùy chọn.

#### Nội dung

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 byte cờ (tùy chọn)
6.  [Date](/docs/specs/common-structures/#date) hết hạn được cắt ngắn từ 8 byte xuống 6
    byte

#### Ghi chú

Kể từ phiên bản 0.7.1.

Trong chế độ "best effort", ngay khi SendMessageExpiresMessage được nhận đầy đủ và nguyên vẹn, router sẽ trả về một MessageStatusMessage thông báo rằng thông điệp đã được chấp nhận để gửi đi. Thông điệp đó sẽ chứa cùng một nonce đã được gửi ở đây. Sau đó, dựa trên các đảm bảo gửi của cấu hình session, router có thể gửi thêm một MessageStatusMessage khác để cập nhật trạng thái.

Kể từ phiên bản 0.8.1, router không gửi Message Status Message nào nếu i2cp.messageReliability=none.

Trước phiên bản 0.9.4, giá trị nonce bằng 0 không được phép. Từ phiên bản 0.9.4 trở đi, giá trị nonce bằng 0 được cho phép và báo cho router rằng nó không nên gửi bất kỳ Message Status Message nào, tức là nó hoạt động như thể i2cp.messageReliability=none chỉ cho thông điệp này.

Trước phiên bản 0.9.14, một session với i2cp.messageReliability=none không thể được ghi đè trên cơ sở từng thông điệp. Kể từ phiên bản 0.9.14, trong một session với i2cp.messageReliability=none, client có thể yêu cầu gửi Message Status Message với kết quả thành công hoặc thất bại của việc gửi bằng cách đặt nonce thành một giá trị khác không. Router sẽ không gửi Message Status Message "accepted" nhưng sau đó sẽ gửi cho client một Message Status Message với cùng nonce và giá trị thành công hoặc thất bại.

#### Trường Flags

Kể từ phiên bản 0.8.4, hai byte trên của Date được định nghĩa lại để chứa các flags. Các flags phải mặc định là tất cả số không để tương thích ngược. Date sẽ không xâm phạm vào trường flags cho đến năm 10889. Các flags có thể được ứng dụng sử dụng để cung cấp gợi ý cho router về việc liệu một LeaseSet và/vagy ElGamal/AES Session Tags có nên được gửi cùng với thông điệp hay không. Các cài đặt này sẽ ảnh hưởng đáng kể đến lượng protocol overhead và độ tin cậy của việc gửi thông điệp. Các bit flag riêng lẻ được định nghĩa như sau, kể từ phiên bản 0.9.2. Các định nghĩa có thể thay đổi. Sử dụng class SendMessageOptions để xây dựng các flags.

Thứ tự bit: 15...0

Bit 15-11

:   Không sử dụng, phải bằng không

Bit 10-9

:   Ghi đè độ tin cậy tin nhắn (Chưa triển khai, sẽ được loại bỏ).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Nếu là 1, không gộp lease set vào garlic encryption cùng với thông điệp này. Nếu

    0, the router may bundle a lease set at its discretion.

Bit 7-4

:   Ngưỡng tag thấp. Nếu có ít hơn số lượng tag này có sẵn,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bits 3-0

:   Số lượng thẻ cần gửi nếu được yêu cầu. Đây chỉ là khuyến nghị và không

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Mô tả

Hướng dẫn client về trạng thái của phiên làm việc.

Được gửi từ Router đến Client, để phản hồi lại [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), hoặc [DestroySessionMessage](#DestroySessionMessage). Trong tất cả các trường hợp, bao gồm cả khi phản hồi [CreateSessionMessage](#CreateSessionMessage), router nên phản hồi ngay lập tức (không chờ các tunnel được xây dựng).

#### Nội dung

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) trạng thái

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Ghi chú

Các giá trị trạng thái được định nghĩa ở trên. Nếu trạng thái là Created, thì Session ID là định danh sẽ được sử dụng cho phần còn lại của phiên.

### SetDateMessage {#SetDateMessage}

#### Mô tả

Ngày và giờ hiện tại. Được gửi từ Router đến Client như một phần của quá trình bắt tay ban đầu. Kể từ phiên bản 0.9.20, cũng có thể được gửi bất kỳ lúc nào sau quá trình bắt tay để thông báo cho client về việc thay đổi đồng hồ.

#### Nội dung

1.  [Date](/docs/specs/common-structures/#date)
2.  Phiên bản I2CP API [String](/docs/specs/common-structures/#string)

#### Ghi chú

Đây thường là tin nhắn đầu tiên được gửi bởi router. Chuỗi phiên bản được bao gồm kể từ bản phát hành 0.8.7. Điều này chỉ hữu ích nếu client và router không ở trong cùng một JVM. Nếu nó không có mặt, router là phiên bản 0.8.6 hoặc cũ hơn.

Các thông điệp SetDate bổ sung sẽ không được gửi đến các client trong cùng một JVM.

## Tài liệu tham khảo

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Tổng quan I2CP](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
