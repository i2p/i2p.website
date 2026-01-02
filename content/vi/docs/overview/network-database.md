---
title: "Cơ sở dữ liệu mạng"
description: "Hiểu về cơ sở dữ liệu mạng phân tán (netDb) của I2P - một DHT (bảng băm phân tán) chuyên biệt dành cho thông tin liên hệ của router và tra cứu đích đến"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Tổng quan

**netDb** là một cơ sở dữ liệu phân tán chuyên biệt, chỉ chứa hai loại dữ liệu: - **RouterInfos** – thông tin liên hệ của router - **LeaseSets** – thông tin liên hệ của destination (đích)

Tất cả dữ liệu đều được ký số và có thể xác minh. Mỗi mục bao gồm thông tin liveliness (tính sống/khả năng hoạt động) nhằm loại bỏ các mục đã lỗi thời và thay thế những mục cũ, giúp bảo vệ trước một số lớp tấn công nhất định.

Việc phân phối sử dụng cơ chế **floodfill**, trong đó một tập con các router duy trì cơ sở dữ liệu phân tán.

---

## 2. RouterInfo (thông tin về router)

Khi các router cần liên lạc với các router khác, chúng trao đổi các gói **RouterInfo** chứa:

- **Định danh Router** – khóa mã hóa, khóa ký, chứng chỉ
- **Địa chỉ liên hệ** – cách để kết nối tới router
- **Dấu thời gian công bố** – thời điểm thông tin này được công bố
- **Các tùy chọn văn bản tùy ý** – cờ khả năng và thiết lập
- **Chữ ký mật mã** – chứng minh tính xác thực

### 2.1 Các cờ khả năng

Các router quảng bá các khả năng thông qua các mã chữ cái trong RouterInfo của chúng:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Phân loại băng thông

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Các giá trị ID mạng

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Thống kê RouterInfo (thông tin về router)

Các router công bố các thống kê tình trạng tùy chọn phục vụ phân tích mạng: - Tỷ lệ xây dựng thành công/từ chối/hết thời gian chờ của Exploratory tunnel (tunnel thăm dò) - Số lượng tunnel tham gia trung bình trong 1 giờ

Các thống kê tuân theo định dạng `stat_(statname).(statperiod)` với các giá trị được phân tách bằng dấu chấm phẩy.

**Ví dụ về số liệu thống kê:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers cũng có thể công bố: `netdb.knownLeaseSets` và `netdb.knownRouters`

### 2.5 Tùy chọn Family (nhóm các router do cùng một đơn vị vận hành)

Kể từ phiên bản 0.9.24, routers có thể khai báo tư cách thành viên family (cùng một người vận hành):

- **family**: Tên family (nhóm router do cùng một nhà vận hành)
- **family.key**: Mã kiểu chữ ký được nối với khóa công khai dùng để ký được mã hóa Base64
- **family.sig**: Chữ ký trên tên family và mã băm router dài 32 byte

Nhiều router trong cùng một family (nhóm các router do cùng một nhà vận hành) sẽ không được sử dụng trong cùng một tunnel.

### 2.6 Hết hạn của RouterInfo (thông tin về router)

- Không hết hạn trong giờ hoạt động đầu tiên
- Không hết hạn khi có 25 hoặc ít hơn RouterInfos (bản ghi thông tin router) được lưu trữ
- Thời hạn hết hạn rút ngắn khi số lượng cục bộ tăng (72 giờ ở mức <120 routers; ~30 giờ ở 300 routers)
- SSU introducers (điểm giới thiệu trong SSU) hết hạn trong ~1 giờ
- Floodfills sử dụng thời hạn 1 giờ cho tất cả RouterInfos cục bộ

---

## 3. LeaseSet

**LeaseSets** mô tả các điểm vào của tunnel cho các đích cụ thể, chỉ rõ:

- **Danh tính router gateway của Tunnel**
- **ID tunnel 4 byte**
- **Thời gian hết hạn của Tunnel**

LeaseSets bao gồm: - **Destination (đích đến)** – khóa mã hóa, khóa ký, chứng chỉ - **Khóa công khai mã hóa bổ sung** – cho garlic encryption đầu-cuối - **Khóa công khai ký bổ sung** – dự kiến dùng cho việc thu hồi (hiện chưa sử dụng) - **Chữ ký mật mã**

### 3.1 Các biến thể LeaseSet (tập hợp lease)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Hết hạn của LeaseSet

Các LeaseSet thông thường sẽ hết hạn tại thời điểm hết hạn lease (bản ghi tunnel) muộn nhất của chúng. Thời điểm hết hạn của LeaseSet2 được chỉ định trong tiêu đề. Thời điểm hết hạn của EncryptedLeaseSet và MetaLeaseSet có thể khác nhau, với khả năng thực thi giới hạn tối đa.

---

## 4. Khởi tạo ban đầu

netDb phi tập trung yêu cầu ít nhất một tham chiếu peer để tham gia mạng. **Reseeding** (khởi tạo mạng ban đầu) lấy các tệp RouterInfo (`routerInfo-$hash.dat`) từ các thư mục netDb của những tình nguyện viên. Lần khởi động đầu tiên tự động lấy từ các URL được ghi cứng trong mã, được chọn ngẫu nhiên.

---

## 5. Cơ chế Floodfill

netDb dạng floodfill sử dụng cơ chế lưu trữ phân tán đơn giản: gửi dữ liệu tới nút floodfill gần nhất. Khi các nút không phải floodfill gửi các bản ghi lưu trữ, các nút floodfill sẽ chuyển tiếp tới một tập con các nút floodfill gần nhất với khóa cụ thể.

Việc tham gia floodfill được biểu thị là một cờ khả năng (`f`) trong RouterInfo.

### 5.1 Các yêu cầu tham gia tự nguyện cho Floodfill

Không giống như các máy chủ thư mục đáng tin cậy được cố định trong mã của Tor, tập hợp floodfill của I2P là **không được tin cậy** và thay đổi theo thời gian.

Floodfill chỉ tự động bật trên các routers có băng thông cao đáp ứng các yêu cầu sau: - Băng thông chia sẻ tối thiểu 128 KBytes/giây (cấu hình thủ công) - Phải vượt qua các kiểm tra tình trạng bổ sung (thời gian hàng đợi thông điệp gửi đi, job lag (độ trễ tác vụ))

Cơ chế tự động tham gia hiện tại dẫn đến khoảng **6% tỷ lệ tham gia floodfill trong mạng**.

Các floodfill (nút đặc biệt của I2P dùng để lưu trữ/phổ biến netDb) được cấu hình thủ công tồn tại song song với các router tự nguyện được kích hoạt tự động. Khi số lượng floodfill giảm xuống dưới ngưỡng, các router băng thông cao sẽ tự động tình nguyện làm floodfill. Khi có quá nhiều floodfill, các router đó sẽ tự bỏ chế độ floodfill.

### 5.2 Các vai trò của Floodfill

Ngoài việc tiếp nhận các yêu cầu lưu trữ netDb và phản hồi các truy vấn, các floodfill thực hiện những chức năng tiêu chuẩn của router. Băng thông cao hơn của chúng thường đồng nghĩa với việc tham gia tunnel nhiều hơn, nhưng điều này không liên quan trực tiếp đến các dịch vụ cơ sở dữ liệu.

---

## 6. Thước đo độ gần trong Kademlia

netDb sử dụng phép đo khoảng cách dựa trên XOR theo **kiểu Kademlia** (một giao thức DHT). Hàm băm SHA256 của RouterIdentity hoặc Destination tạo ra khóa Kademlia (ngoại trừ LS2 Encrypted LeaseSets, vốn sử dụng SHA256 của byte loại 3 cộng với khóa công khai được làm mù).

### 6.1 Luân chuyển không gian khóa

Để tăng chi phí cho các cuộc tấn công Sybil, thay vì sử dụng `SHA256(key)`, hệ thống sử dụng:

```
SHA256(key + yyyyMMdd)
```
trong đó ngày là một chuỗi ASCII 8 byte biểu diễn ngày UTC. Điều này tạo ra **routing key** (khóa định tuyến), thay đổi hằng ngày vào nửa đêm UTC—gọi là **keyspace rotation** (luân phiên không gian khóa).

Các khóa định tuyến không bao giờ được truyền trong các thông điệp I2NP; chúng chỉ được dùng để xác định khoảng cách cục bộ.

---

## 7. Phân đoạn Cơ sở dữ liệu mạng (netDb)

Các DHT Kademlia truyền thống không duy trì tính không thể liên kết của thông tin được lưu trữ. I2P ngăn chặn các cuộc tấn công nhằm liên kết các tunnel phía client với các router bằng cách triển khai **phân đoạn**.

### 7.1 Chiến lược phân đoạn

Các router theo dõi: - Liệu các bản ghi đến qua tunnel của client hay trực tiếp - Nếu qua tunnel, là tunnel/destination (đích) của client nào - Nhiều lần đến qua tunnel đều được theo dõi - Phân biệt phản hồi lưu trữ và phản hồi tra cứu

Cả hai triển khai Java và C++ đều sử dụng: - Một **"Main" netDb** để tra cứu trực tiếp/các thao tác floodfill trong ngữ cảnh router - **"Client Network Databases"** hoặc **"Sub-Databases"** trong ngữ cảnh client, thu nhận các bản ghi được gửi tới các tunnel của client

Các netDb của ứng dụng khách chỉ tồn tại trong suốt vòng đời của ứng dụng khách, và chỉ chứa các mục tunnel của ứng dụng khách. Các mục từ các tunnel của ứng dụng khách không được trùng lặp với các lượt đến trực tiếp.

Mỗi netDb theo dõi liệu các mục đến dưới dạng store (thông điệp lưu trữ) — sẽ phản hồi các yêu cầu tra cứu — hay dưới dạng lookup reply (phản hồi tra cứu), trường hợp này chỉ phản hồi nếu trước đó đã được lưu tới cùng một Destination (đích trong I2P). Các client không bao giờ trả lời truy vấn bằng các mục Main netDb, mà chỉ bằng các mục trong cơ sở dữ liệu mạng của client.

Các chiến lược kết hợp **phân đoạn** netDb để chống lại các cuộc tấn công nhằm liên kết client với router.

---

## 8. Lưu trữ, xác minh và tra cứu

### 8.1 Lưu trữ RouterInfo (thông tin router) tới các nút

I2NP `DatabaseStoreMessage` chứa RouterInfo cục bộ được trao đổi trong quá trình khởi tạo kết nối truyền tải NTCP hoặc SSU.

### 8.2 Lưu trữ LeaseSet tới các nút ngang hàng

Các I2NP `DatabaseStoreMessage` chứa LeaseSet cục bộ được trao đổi định kỳ qua các thông điệp được mã hóa bằng garlic encryption, được gói kèm với lưu lượng Destination (đích I2P), cho phép phản hồi mà không cần tra cứu LeaseSet.

### 8.3 Lựa chọn Floodfill (router đặc biệt trong I2P để lưu trữ và phổ biến netDb)

`DatabaseStoreMessage` gửi tới floodfill gần nhất so với khóa định tuyến hiện tại. Floodfill gần nhất được tìm qua tra cứu trong cơ sở dữ liệu cục bộ. Ngay cả khi không thực sự gần nhất, flooding (cơ chế phát tán diện rộng) sẽ lan truyền nó "gần hơn" bằng cách gửi tới nhiều floodfill.

Kademlia truyền thống (một giao thức bảng băm phân tán - DHT) sử dụng tìm kiếm 'find-closest' trước khi chèn. Trong khi I2NP không có các thông điệp như vậy, các router có thể thực hiện tìm kiếm lặp từng bước với bit ít ý nghĩa nhất được đảo (`key ^ 0x01`) để bảo đảm tìm ra nút gần nhất chính xác.

### 8.4 Lưu trữ RouterInfo tới các Floodfill

Các router công bố RouterInfo bằng cách kết nối trực tiếp tới một floodfill, gửi I2NP `DatabaseStoreMessage` với Reply Token (mã thông báo phản hồi) khác 0. Thông điệp không được garlic encrypted end-to-end (kết nối trực tiếp, không có trung gian). Floodfill phản hồi bằng `DeliveryStatusMessage`, sử dụng Reply Token làm Message ID (ID thông điệp).

Các router cũng có thể gửi RouterInfo (thông tin về router) thông qua tunnel thăm dò (giới hạn kết nối, không tương thích, ẩn IP). Các floodfill có thể từ chối các yêu cầu lưu trữ như vậy khi quá tải.

### 8.5 Lưu trữ LeaseSet tới các Floodfills

Việc lưu trữ LeaseSet (bộ mô tả đích trong I2P) nhạy cảm hơn so với RouterInfo (thông tin nhận dạng của router). Các router (nút I2P) phải ngăn chặn việc liên kết LeaseSet với chính chúng.

Routers công bố LeaseSet bằng cách gửi `DatabaseStoreMessage` qua tunnel client đi ra, với Reply Token (mã thông báo phản hồi) khác 0. Thông điệp được mã hóa end-to-end bằng garlic encryption sử dụng Session Key Manager (trình quản lý khóa phiên) của Destination (đích I2P), che giấu khỏi điểm cuối đi ra của tunnel. Floodfill phản hồi bằng `DeliveryStatusMessage` được trả về qua tunnel đi vào.

### 8.6 Quy trình phát tán

Các floodfill xác thực RouterInfo (thông tin router)/LeaseSet bằng các tiêu chí thích ứng phụ thuộc vào tải, kích thước netdb và các yếu tố khác trước khi lưu cục bộ.

Sau khi nhận được dữ liệu mới hơn hợp lệ, các floodfill "flood" nó bằng cách tìm 3 router floodfill gần nhất so với khóa định tuyến. Các kết nối trực tiếp gửi I2NP `DatabaseStoreMessage` với Reply Token (mã phản hồi) bằng 0. Các router khác không phản hồi hay flood lại.

**Ràng buộc quan trọng:** - Floodfills không được phát tán qua tunnels; chỉ kết nối trực tiếp - Floodfills không bao giờ phát tán LeaseSet đã hết hạn hoặc RouterInfo được công bố hơn một giờ trước

### 8.7 Tra cứu RouterInfo và LeaseSet

I2NP `DatabaseLookupMessage` yêu cầu các bản ghi netdb từ các router floodfill. Các tra cứu được gửi qua tunnel thăm dò đi ra; phản hồi chỉ định tunnel thăm dò đi vào để trả về.

Các lần tra cứu thường được gửi song song tới hai floodfill routers "tốt" gần nhất với khóa được yêu cầu.

- **Khớp cục bộ**: nhận phản hồi I2NP `DatabaseStoreMessage`
- **Không có khớp cục bộ**: nhận I2NP `DatabaseSearchReplyMessage` với các tham chiếu router floodfill khác gần với khóa

Tra cứu LeaseSet sử dụng garlic encryption đầu-cuối (kể từ phiên bản 0.9.5). Việc tra cứu RouterInfo (thông tin router) không được mã hóa do chi phí tính toán của ElGamal, khiến chúng dễ bị nghe lén tại điểm cuối hướng ra.

Kể từ phiên bản 0.9.7, các phản hồi tra cứu bao gồm khóa phiên và thẻ, nhằm che giấu phản hồi khỏi cổng vào.

### 8.8 Tra cứu lặp

Trước 0.8.9: Hai tra cứu dự phòng song song không có định tuyến đệ quy hoặc lặp.

Từ 0.8.9: **Tra cứu lặp (iterative lookups)** được triển khai không dư thừa—hiệu quả hơn, đáng tin cậy hơn, và phù hợp với kiến thức floodfill không đầy đủ. Khi mạng phát triển và routers biết ít floodfill hơn, các lần tra cứu tiệm cận độ phức tạp O(log n).

Tra cứu lặp vẫn tiếp tục ngay cả khi không có tham chiếu đến nút ngang hàng gần hơn, ngăn chặn black-holing độc hại (chuyển vào “hố đen” để loại bỏ). Các giới hạn hiện hành về số lượng truy vấn tối đa và thời gian chờ vẫn được áp dụng.

### 8.9 Xác minh

**Xác minh RouterInfo (thông tin của router)**: Đã bị vô hiệu hóa kể từ 0.9.7.1 để ngăn chặn các cuộc tấn công được mô tả trong bài báo "Practical Attacks Against the I2P Network".

**LeaseSet Verification**: Các router chờ ~10 giây, rồi thực hiện tra cứu từ một floodfill khác thông qua tunnel máy khách đi ra. Garlic encryption đầu-cuối (cơ chế mã hóa "garlic" gộp nhiều thông điệp) ẩn khỏi điểm cuối đi ra. Phản hồi quay về qua các tunnel đi vào.

Kể từ 0.9.7, các phản hồi được mã hóa bằng session key/tag (khóa phiên/thẻ phiên), ẩn khỏi inbound gateway (cổng vào).

### 8.10 Thăm dò

**Thăm dò** liên quan đến tra cứu netdb với các khóa ngẫu nhiên để khám phá các router mới. Các floodfill phản hồi bằng `DatabaseSearchReplyMessage` chứa các băm router không phải floodfill gần với khóa được yêu cầu. Các truy vấn thăm dò đặt một cờ đặc biệt trong `DatabaseLookupMessage`.

---

## 9. MultiHoming (đa kết nối)

Các Destination (địa chỉ đích trong I2P) sử dụng cùng một cặp khóa riêng/công khai (theo cách truyền thống qua `eepPriv.dat`) có thể chạy trên nhiều router đồng thời. Mỗi thể hiện sẽ định kỳ công bố các LeaseSets đã được ký; LeaseSet được công bố gần đây nhất sẽ được trả về cho các yêu cầu tra cứu. Với thời gian sống tối đa của LeaseSet là 10 phút, sự gián đoạn kéo dài nhiều nhất khoảng ~10 phút.

Kể từ 0.9.38, **Meta LeaseSets** hỗ trợ các dịch vụ multihomed (kết nối nhiều mạng/địa chỉ) quy mô lớn, sử dụng các Destinations (điểm đích) riêng biệt cung cấp các dịch vụ chung. Các bản ghi trong Meta LeaseSet là các Destinations hoặc các Meta LeaseSets khác với thời hạn hiệu lực tối đa 18.2 giờ, cho phép hàng trăm/hàng nghìn Destinations cung cấp các dịch vụ chung.

---

## 10. Phân tích mối đe dọa

Hiện có khoảng 1700 floodfill routers (các router đặc biệt dùng để lưu trữ và phân phối netDb) đang hoạt động. Sự phát triển của mạng khiến phần lớn các cuộc tấn công trở nên khó thực hiện hơn hoặc ít gây tác động hơn.

### 10.1 Biện pháp giảm thiểu chung

- **Tăng trưởng**: Nhiều floodfill (nút đặc biệt lưu trữ netdb) hơn khiến các cuộc tấn công khó hơn hoặc ít tác động hơn
- **Dự phòng**: Tất cả các mục netdb (cơ sở dữ liệu mạng của I2P) được lưu trữ trên 3 floodfill routers gần khóa nhất thông qua flooding
- **Chữ ký**: Tất cả các mục đều được ký bởi người tạo; việc giả mạo là không thể

### 10.2 Router chậm hoặc không phản hồi

Các router duy trì các thống kê hồ sơ peer mở rộng cho các floodfill: - Thời gian phản hồi trung bình - Tỷ lệ truy vấn được trả lời - Tỷ lệ thành công xác minh lưu trữ - Lần lưu trữ thành công gần nhất - Lần tra cứu thành công gần nhất - Phản hồi gần nhất

Các router sử dụng các chỉ số này khi xác định "goodness" (mức độ tốt) để chọn floodfill gần nhất. Các router hoàn toàn không phản hồi được nhanh chóng nhận diện và tránh; các router độc hại ở mức độ nhất định đặt ra thách thức lớn hơn.

### 10.3 Tấn công Sybil (toàn bộ không gian khóa)

Những kẻ tấn công có thể tạo ra nhiều floodfill routers được phân tán khắp không gian khóa như một phương thức tấn công từ chối dịch vụ (DoS) hiệu quả.

Nếu không hành xử sai trái đủ mức để được gán nhãn "bad", các biện pháp có thể bao gồm: - Biên soạn các danh sách hash/IP của router (nút trong I2P) xấu được thông báo qua bản tin bảng điều khiển, website, diễn đàn - Bật floodfill (router đặc biệt lưu trữ netDb) trên toàn mạng ("chống Sybil bằng nhiều Sybil hơn") - Các phiên bản phần mềm mới với các danh sách "bad" cố định trong mã - Cải thiện các số đo và ngưỡng trong hồ sơ peer để nhận diện tự động - Tiêu chí khối IP loại trừ nhiều floodfill trong cùng một khối IP - Danh sách đen tự động dựa trên đăng ký (tương tự đồng thuận của Tor)

Các mạng lớn hơn khiến việc này khó hơn.

### 10.4 Tấn công Sybil (Không gian khóa một phần)

Kẻ tấn công có thể tạo 8–15 router floodfill được gom cụm gần nhau trong không gian khóa. Mọi thao tác tra cứu/lưu trữ đối với không gian khóa đó sẽ được định tuyến tới các router của kẻ tấn công, tạo điều kiện cho tấn công từ chối dịch vụ (DoS) nhắm vào các trang I2P cụ thể.

Vì không gian khóa lập chỉ mục các hàm băm mật mã SHA-256, kẻ tấn công cần dùng vét cạn (brute-force) để tạo ra các routers có độ gần đủ.

**Phòng thủ**: Thuật toán đo độ gần Kademlia (thuật toán DHT) thay đổi theo thời gian bằng `SHA256(key + YYYYMMDD)`, cập nhật hằng ngày vào lúc nửa đêm UTC. Việc **xoay vòng không gian khóa** này buộc kẻ tấn công phải tái khởi tạo cuộc tấn công mỗi ngày.

> **Note**: Nghiên cứu gần đây cho thấy việc xoay vòng không gian khóa không mấy hiệu quả—kẻ tấn công có thể tiền tính các băm của router, chỉ cần vài router để chiếm lĩnh các phần của không gian khóa trong vòng nửa giờ sau khi xoay vòng.

Hệ quả của việc xoay vòng hằng ngày: netdb phân tán trở nên không đáng tin cậy trong vài phút sau khi xoay vòng—các lần tra cứu thất bại trước khi router gần nhất mới nhận được các stores (thông điệp lưu trữ).

### 10.5 Tấn công Bootstrap (khởi tạo)

Kẻ tấn công có thể chiếm quyền kiểm soát các trang web reseed (trang web cung cấp dữ liệu khởi động ban đầu cho router mới) hoặc đánh lừa các nhà phát triển thêm các trang web reseed độc hại, khiến các router mới khởi động vào các mạng bị cô lập hoặc do đa số kiểm soát.

**Các biện pháp phòng thủ đã triển khai:** - Lấy các tập con RouterInfo từ nhiều trang reseed thay vì một trang duy nhất - Giám sát reseed ngoài mạng, định kỳ thăm dò các trang - Kể từ 0.9.14, các gói dữ liệu reseed dưới dạng tệp zip có chữ ký, kèm xác minh chữ ký được tải về (xem [đặc tả su3](/docs/specs/updates))

### 10.6 Thu thập truy vấn

Floodfill routers có thể "chuyển hướng" các nút ngang hàng tới các routers do kẻ tấn công kiểm soát thông qua các tham chiếu được trả về.

Ít có khả năng thông qua thăm dò do tần suất thấp; routers chủ yếu thu được các tham chiếu đồng cấp thông qua việc xây dựng tunnel thông thường.

Kể từ 0.8.9, đã triển khai cơ chế tra cứu lặp. Các tham chiếu floodfill trong `DatabaseSearchReplyMessage` sẽ được lần theo nếu chúng gần với khóa tra cứu hơn. Các router gửi yêu cầu không tin cậy mức độ “gần” của tham chiếu. Việc tra cứu vẫn tiếp tục ngay cả khi không có khóa nào gần hơn cho đến khi hết thời gian chờ/số truy vấn tối đa, nhằm ngăn chặn hành vi black-holing (cố ý làm truy vấn “mất hút”).

### 10.7 Rò rỉ thông tin

Rò rỉ thông tin DHT (bảng băm phân tán) trong I2P cần được điều tra thêm. Floodfill routers có thể quan sát các truy vấn để thu thập thông tin. Khi tỷ lệ nút độc hại đạt 20%, các mối đe dọa Sybil được mô tả trước đó trở nên đáng lo ngại vì nhiều lý do.

---

## 11. Công việc tương lai

- Mã hóa đầu-cuối cho các tra cứu và phản hồi netDb bổ sung
- Các phương pháp theo dõi phản hồi tra cứu tốt hơn
- Các phương pháp giảm thiểu cho các vấn đề độ tin cậy liên quan đến luân chuyển không gian khóa

---

## 12. Tài liệu tham khảo

- [Đặc tả Cấu trúc Chung](/docs/specs/common-structures/) – Các cấu trúc RouterInfo (thông tin router) và LeaseSet
- [Đặc tả I2NP](/docs/specs/i2np/) – Các loại thông điệp cơ sở dữ liệu
- [Đề xuất 123: Các bản ghi netDb mới](/proposals/123-new-netdb-entries) – Đặc tả LeaseSet2 (phiên bản thứ hai của LeaseSet)
- [Thảo luận netDb trong lịch sử](/docs/netdb/) – Lịch sử phát triển và các thảo luận đã lưu trữ
