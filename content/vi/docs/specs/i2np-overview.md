---
title: "Tổng quan về I2NP"
description: "Tổng quan về Giao thức Mạng I2P (I2NP) - định dạng tin nhắn, các loại, độ ưu tiên và giới hạn kích thước."
slug: "i2np-overview"
aliases:
  - "/vi/docs/protocol/i2np"
  - "/vi/docs/protocol/i2np/"
category: "Giao thức"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Tổng quan

Giao thức Mạng I2P (I2NP), nằm giữa I2CP và các giao thức truyền tải I2P khác nhau, quản lý việc định tuyến và trộn lẫn các thông điệp giữa các bộ định tuyến, cũng như việc lựa chọn giao thức truyền tải nào sử dụng khi giao tiếp với một máy ngang hàng mà cả hai bên cùng hỗ trợ nhiều giao thức truyền tải.

## Định nghĩa I2NP

Các tin nhắn I2NP (I2P Network Protocol) có thể được sử dụng cho các tin nhắn một bước nhảy, từ router đến router, điểm-điểm. Bằng cách mã hóa và gói các tin nhắn vào bên trong các tin nhắn khác, chúng có thể được gửi một cách an toàn qua nhiều bước nhảy đến đích cuối cùng. Độ ưu tiên chỉ được sử dụng cục bộ tại điểm khởi tạo, ví dụ: khi xếp hàng đợi để gửi đi.

Các mức độ ưu tiên được liệt kê bên dưới có thể không còn cập nhật và có thể thay đổi. Việc triển khai hàng đợi ưu tiên có thể khác nhau.

## Định dạng tin nhắn {#format}

Bảng dưới đây mô tả phần tiêu đề truyền thống 16 byte được sử dụng trong NTCP. Các giao thức truyền tải SSU và NTCP2 sử dụng các tiêu đề đã được sửa đổi.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Type</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unique ID</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Checksum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 - 61.2KB</td>
</tr>
</table>
Mặc dù kích thước tải trọng tối đa danh nghĩa là 64KB, kích thước này còn bị giới hạn hơn nữa bởi phương pháp phân mảnh các tin nhắn I2NP thành nhiều tin nhắn đường hầm 1KB như được mô tả trên trang [triển khai đường hầm](/docs/specs/tunnel-implementation/).

Số lượng phân mảnh tối đa là 64, và thông điệp có thể không được căn chỉnh hoàn hảo, do đó thông điệp phải vừa đủ trong 63 phân mảnh theo quy định.

Kích thước tối đa của một đoạn ban đầu là 956 byte (giả sử ở chế độ giao hàng TUNNEL); kích thước tối đa của một đoạn tiếp theo là 996 byte. Do đó, kích thước tối đa vào khoảng 956 + (62 × 996) = 62708 byte, hay 61,2 KB.

Ngoài ra, các giao thức truyền tải có thể có các giới hạn bổ sung. Giới hạn NTCP là 16KB - 6 = 16378 byte. Giới hạn SSU là khoảng 32 KB. Giới hạn NTCP2 là khoảng 64KB - 20 = 65516 byte, cao hơn mức mà một tunnel có thể hỗ trợ.

Lưu ý rằng đây không phải là giới hạn đối với các gói tin mà client nhìn thấy, vì router có thể gom gói thuê (leaseset) phản hồi và/hoặc các thẻ phiên (session tags) cùng với tin nhắn của client vào một tin nhắn garlic. Kích thước của gói thuê và các thẻ cộng lại có thể làm tăng khoảng 5,5KB. Do đó, giới hạn gói tin hiện tại vào khoảng 10KB. Giới hạn này sẽ được tăng lên trong một bản phát hành tương lai.

## Các loại tin nhắn {#types}

Độ ưu tiên có số cao hơn thì mức ưu tiên càng cao. Phần lớn lưu lượng là TunnelDataMessages (độ ưu tiên 400), do đó mọi thứ trên 400 về cơ bản là ưu tiên cao, và mọi thứ dưới đó là ưu tiên thấp. Lưu ý thêm rằng nhiều tin nhắn thường được định tuyến thông qua các tunnel thăm dò (exploratory tunnels), chứ không phải tunnel khách hàng (client tunnels), và do đó có thể không nằm trong cùng một hàng đợi trừ khi các bước nhảy đầu tiên tình cờ nằm trên cùng một peer.

Ngoài ra, không phải tất cả các loại tin nhắn đều được gửi mà không mã hóa. Ví dụ, khi kiểm tra một tunnel, router sẽ bao bọc một DeliveryStatusMessage, được đặt bên trong một GarlicMessage, và tiếp tục được bao bọc bởi một DataMessage.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Priority</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Comments</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookupMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">May vary</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseSearchReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Typ. 161</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Size is 65 + 32*(number of hashes) where typically, the hashes for three floodfill routers are returned.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseStoreMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Varies</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">460</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet. RouterInfo structures are compressed, and size varies; however there is a continuing effort to reduce the amount of data published in a RouterInfo.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4 - 62080</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">425</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary on a per-destination basis</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DeliveryStatusMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Used for message replies, and for testing tunnels - generally wrapped in a GarlicMessage</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/overview/garlic-routing/">GarlicMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generally wrapped in a DataMessage - but when unwrapped, given a priority of 100 by the forwarding router</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelDataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1028</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The most common message. Priority for tunnel participants, outbound endpoints, and inbound gateways was reduced to 200 as of release 0.6.1.33. Outbound gateway messages (i.e. those originated locally) remains at 400.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelGatewayMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300/400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildReplyMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Others (Types 0, 4-9, 12)</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">0, 4-9, 12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Obsolete, Unused</td>
</tr>
</table>
## Kiểm tra tunnel

Việc kiểm tra tunnel là bắt buộc kể từ phiên bản API 0.9.68 năm 2026-02, vì các router được phép hủy các tunnel đang tham gia nếu không nhận được lưu lượng nào sau hai phút đầu tiên.

## Thông số kỹ thuật giao thức đầy đủ

Xem trang [Thông số kỹ thuật I2NP](/docs/specs/i2np/) để biết thông số giao thức đầy đủ. Xem thêm trang [Thông số kỹ thuật Cấu trúc Dữ liệu Chung](/docs/specs/common-structures/).

## Công việc trong tương lai

Chưa rõ liệu sơ đồ ưu tiên hiện tại có hiệu quả nói chung hay không, và liệu các mức ưu tiên cho các tin nhắn khác nhau có cần được điều chỉnh thêm hay không. Đây là chủ đề cần nghiên cứu, phân tích và thử nghiệm thêm.
