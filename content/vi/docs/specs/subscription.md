---
title: "Các lệnh cho nguồn cấp đăng ký địa chỉ"
description: "Phần mở rộng cho các nguồn cấp đăng ký địa chỉ, cho phép chủ sở hữu hostname (tên máy chủ) cập nhật và quản lý các bản ghi của họ"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Tổng quan

Đặc tả này mở rộng address subscription feed (nguồn cấp đăng ký địa chỉ) bằng các lệnh, cho phép các máy chủ tên phát quảng bá các cập nhật mục từ các chủ sở hữu hostname (tên máy chủ). Được đề xuất ban đầu trong [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (tháng 9 năm 2014), được hiện thực trong phiên bản 0.9.26 (tháng 6 năm 2016), và được triển khai trên toàn mạng với trạng thái CLOSED.

Hệ thống đã duy trì ổn định và không thay đổi kể từ khi triển khai ban đầu, tiếp tục vận hành giống hệt trong I2P 2.10.0 (Router API 0.9.65, tháng 9 năm 2025).

## Động lực

Trước đây, các máy chủ đăng ký hosts.txt chỉ gửi dữ liệu dưới dạng hosts.txt đơn giản:

```
example.i2p=b64destination
```
Định dạng cơ bản này đã tạo ra một số vấn đề:

- Chủ sở hữu tên máy chủ không thể cập nhật Destination (địa chỉ/định danh trên I2P) gắn với các tên máy chủ của họ (ví dụ, để nâng cấp khóa ký lên kiểu mật mã mạnh hơn).
- Chủ sở hữu tên máy chủ không thể tùy ý từ bỏ tên máy chủ của họ. Họ phải chuyển trực tiếp các khóa riêng tư của Destination tương ứng cho người sở hữu mới.
- Không có cách nào để xác thực rằng một tên miền con được kiểm soát bởi tên máy chủ gốc tương ứng. Hiện điều này chỉ được một số máy chủ tên thực thi riêng lẻ.

## Thiết kế

Đặc tả này bổ sung các dòng lệnh vào định dạng hosts.txt. Với các lệnh này, các máy chủ tên có thể mở rộng dịch vụ của họ để cung cấp các tính năng bổ sung. Các máy khách triển khai đặc tả này có thể lắng nghe các tính năng đó thông qua quy trình đăng ký thông thường.

Tất cả các dòng lệnh phải được ký bởi Destination tương ứng (định danh đích trong I2P). Điều này đảm bảo rằng các thay đổi chỉ được thực hiện theo yêu cầu của chủ sở hữu hostname.

## Hệ quả về bảo mật

Đặc tả này không ảnh hưởng đến tính ẩn danh.

Có sự gia tăng rủi ro liên quan đến việc mất quyền kiểm soát một khóa Destination, vì ai đó có được nó có thể dùng các lệnh này để thay đổi bất kỳ tên máy chủ nào được liên kết. Tuy nhiên, điều này không gây vấn đề nhiều hơn so với hiện trạng, nơi mà người nào có được một Destination (địa chỉ đích trong I2P) có thể giả mạo một tên máy chủ và (một phần) chiếm quyền kiểm soát lưu lượng của nó. Rủi ro tăng thêm được cân bằng bằng cách trao cho người sở hữu tên máy chủ khả năng thay đổi Destination gắn với một tên máy chủ trong trường hợp họ tin rằng Destination đã bị xâm phạm. Điều này là không thể với hệ thống hiện tại.

## Đặc tả

### Các Kiểu Dòng Mới

Có hai loại dòng mới:

1. **Các lệnh Add và Change:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Các lệnh xóa:**

```
#!key1=val1#key2=val2...
```
#### Thứ tự

Một nguồn cấp dữ liệu không nhất thiết theo đúng thứ tự hoặc đầy đủ. Ví dụ, một lệnh change có thể xuất hiện trên một dòng trước một lệnh add, hoặc không kèm theo lệnh add.

Các khóa có thể ở bất kỳ thứ tự nào. Không cho phép các khóa trùng lặp. Tất cả các khóa và giá trị đều phân biệt chữ hoa chữ thường.

### Các khóa phổ biến

**Bắt buộc trong tất cả các lệnh:**

**sig** : Chữ ký Base64, sử dụng khóa ký của đích

**Tham chiếu đến tên máy chủ thứ hai và/hoặc đích:**

**oldname** : Một tên máy chủ thứ hai (mới hoặc đã thay đổi)

**olddest** : Một đích Base64 thứ hai (mới hoặc đã thay đổi)

**oldsig** : Một chữ ký Base64 thứ hai, sử dụng khóa ký từ olddest

**Các khóa thường gặp khác:**

**action** : Một lệnh

**name** : Tên máy chủ, chỉ xuất hiện nếu phía trước không có `example.i2p=b64dest`

**dest** : Đích Base64, chỉ xuất hiện nếu trước đó không có `example.i2p=b64dest`

**date** : Tính bằng số giây kể từ Unix epoch (mốc thời gian Unix)

**expires** : Tính bằng giây kể từ epoch (mốc thời gian Unix)

### Lệnh

Tất cả các lệnh ngoại trừ lệnh "Add" phải chứa một `action=command` cặp khóa/giá trị.

Để tương thích với các ứng dụng khách cũ, hầu hết các lệnh đều được đặt trước bởi `example.i2p=b64dest`, như nêu bên dưới. Đối với các mục thay đổi, các giá trị hiển thị luôn là giá trị mới. Mọi giá trị cũ được đưa vào phần key/value.

Các khóa được liệt kê là bắt buộc. Mọi lệnh có thể chứa các mục khóa/giá trị bổ sung không được định nghĩa ở đây.

#### Thêm tên máy chủ

**Được đặt trước bởi example.i2p=b64dest** : CÓ, đây là tên máy chủ và đích đến mới.

**hành động** : KHÔNG được bao gồm, nó được ngầm hiểu.

**sig** : chữ ký số

Ví dụ:

```
example.i2p=b64dest#!sig=b64sig
```
#### Thay đổi tên máy chủ

**Được đặt trước bởi example.i2p=b64dest** : CÓ, đây là tên máy chủ mới và đích cũ.

**hành động** : changename

**oldname** : tên máy chủ cũ, sẽ được thay thế

**sig** : chữ ký số

Ví dụ:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Thay đổi điểm đích

**Preceded by example.i2p=b64dest** : CÓ, đây là tên máy chủ cũ và đích mới.

**hành động** : changedest

**olddest** : điểm đến cũ, sẽ được thay thế

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký số

Ví dụ:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Thêm bí danh cho tên máy chủ

**Có tiền tố example.i2p=b64dest** : CÓ, đây là tên máy chủ mới (bí danh) và điểm đích cũ.

**hành động** : addname

**oldname** : tên máy chủ cũ

**sig** : chữ ký số

Ví dụ:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Thêm bí danh cho địa chỉ đích

(Được dùng để nâng cấp mật mã)

**Được đặt trước bởi example.i2p=b64dest** : CÓ, đây là tên máy chủ cũ và đích đến mới (thay thế).

**action** : adddest

**olddest** : đích cũ

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký sử dụng dest

Ví dụ:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Thêm tên miền phụ

**Được đặt trước bởi subdomain.example.i2p=b64dest** : CÓ, đây là tên miền con và Destination (đích I2P) mới.

**hành động** : addsubdomain

**oldname** : tên máy chủ cấp cao hơn (example.i2p)

**olddest** : đích cấp cao hơn (ví dụ example.i2p)

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký sử dụng dest

Ví dụ:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Cập nhật siêu dữ liệu

**Được đặt trước bởi example.i2p=b64dest** : CÓ, đây là tên máy chủ và destination (đích đến) cũ.

**hành động** : cập nhật

**sig** : chữ ký

(thêm các khóa đã cập nhật tại đây)

Ví dụ:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Xóa tên máy chủ

**Có tiền tố example.i2p=b64dest** : KHÔNG, những mục này được chỉ định trong các tùy chọn

**hành động** : xóa

**name** : tên máy chủ

**dest** : điểm đích

**sig** : chữ ký

Ví dụ:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Xóa tất cả liên quan đến điểm đến này

**Có tiền tố example.i2p=b64dest** : KHÔNG, những mục này được chỉ định trong các tùy chọn

**action** : removeall

**dest** : đích đến

**sig** : chữ ký

Ví dụ:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Chữ ký

Mọi lệnh phải được ký số bởi Destination (đích I2P) tương ứng. Các lệnh có hai Destination có thể cần hai chữ ký số.

`oldsig` luôn là chữ ký "bên trong". Ký và xác minh khi không có các khóa `oldsig` hoặc `sig`. `sig` luôn là chữ ký "bên ngoài". Ký và xác minh khi có khóa `oldsig` nhưng không có khóa `sig`.

#### Đầu vào cho chữ ký

Để tạo một luồng byte nhằm tạo hoặc xác minh chữ ký, hãy tuần tự hóa theo cách sau:

1. Xóa khóa `sig`
2. Nếu xác minh bằng `oldsig`, cũng xóa khóa `oldsig`
3. Chỉ đối với các lệnh Add hoặc Change, xuất `example.i2p=b64dest`
4. Nếu còn bất kỳ khóa nào, xuất `#!`
5. Sắp xếp các tùy chọn theo khóa UTF-8, báo lỗi nếu có khóa trùng lặp
6. Với mỗi cặp khóa/giá trị, xuất `key=value`, theo sau bởi (nếu không phải cặp khóa/giá trị cuối cùng) một ký tự `#`

**Ghi chú**

- Không xuất ký tự xuống dòng
- Bảng mã đầu ra là UTF-8
- Tất cả việc mã hóa destination và signature là Base 64, sử dụng bảng chữ cái của I2P
- Khóa và giá trị phân biệt chữ hoa/thường
- Tên máy chủ phải ở dạng chữ thường

#### Các loại chữ ký hiện tại

Kể từ I2P 2.10.0, các loại chữ ký sau được hỗ trợ cho Destination (địa chỉ đích):

- **EdDSA_SHA512_Ed25519** (Type 7): Phổ biến nhất cho các đích (Destination) kể từ 0.9.15. Sử dụng khóa công khai 32 byte và chữ ký 64 byte. Đây là kiểu chữ ký được khuyến nghị cho các đích mới.
- **RedDSA_SHA512_Ed25519** (Type 13): Chỉ khả dụng cho các đích và leasesets được mã hóa (kể từ 0.9.39).
- Các kiểu kế thừa (DSA_SHA1, các biến thể ECDSA): Vẫn được hỗ trợ nhưng không còn được khuyến nghị cho các Router Identities mới kể từ 0.9.58.

Lưu ý: Các tùy chọn mật mã hậu lượng tử đã có sẵn kể từ I2P 2.10.0 nhưng vẫn chưa phải là các loại chữ ký mặc định.

## Tính tương thích

Tất cả các dòng mới trong định dạng hosts.txt được triển khai bằng cách sử dụng các ký tự chú thích đầu dòng (`#!`), vì vậy mọi phiên bản I2P cũ sẽ xem các lệnh mới là chú thích và bỏ qua chúng một cách an toàn.

Khi các router I2P cập nhật lên đặc tả mới, chúng sẽ không diễn giải lại các chú thích cũ, mà sẽ bắt đầu lắng nghe các lệnh mới trong các lần tải về tiếp theo đối với nguồn đăng ký của chúng. Vì vậy, điều quan trọng là các máy chủ tên cần lưu giữ các mục lệnh bằng một cách nào đó, hoặc bật hỗ trợ ETag để các router có thể tải về tất cả các lệnh trước đây.

## Trạng thái triển khai

**Triển khai ban đầu:** Phiên bản 0.9.26 (ngày 7 tháng 6 năm 2016)

**Trạng thái hiện tại:** Ổn định và không thay đổi đến I2P 2.10.0 (Router API 0.9.65, tháng 9 năm 2025)

**Trạng thái đề xuất:** ĐÃ ĐÓNG (được triển khai thành công trên toàn mạng)

**Vị trí hiện thực:** `apps/addressbook/java/src/net/i2p/addressbook/` trong I2P Java router

**Các lớp chính:** - `SubscriptionList.java`: Quản lý việc xử lý đăng ký - `Subscription.java`: Xử lý các nguồn cấp đăng ký riêng lẻ - `AddressBook.java`: Chức năng cốt lõi của sổ địa chỉ - `Daemon.java`: Dịch vụ nền của sổ địa chỉ

**URL đăng ký mặc định:** `http://i2p-projekt.i2p/hosts.txt`

## Chi tiết về phương thức truyền tải

Các đăng ký sử dụng HTTP với hỗ trợ GET có điều kiện:

- **Header ETag:** Hỗ trợ phát hiện thay đổi hiệu quả
- **Header Last-Modified:** Theo dõi thời điểm cập nhật đăng ký
- **304 Not Modified:** Máy chủ nên trả về mã này khi nội dung chưa thay đổi
- **Content-Length:** Rất khuyến nghị áp dụng cho mọi phản hồi

I2P router sử dụng hành vi HTTP client tiêu chuẩn với hỗ trợ bộ nhớ đệm thích hợp.

## Ngữ cảnh phiên bản

**Ghi chú về phiên bản I2P:** Bắt đầu từ khoảng phiên bản 1.5.0 (tháng 8 năm 2021), I2P đã chuyển từ 0.9.x sang semantic versioning (đánh số phiên bản ngữ nghĩa) với các phiên bản 1.x, 2.x, v.v. Tuy nhiên, phiên bản Router API nội bộ tiếp tục sử dụng cách đánh số 0.9.x để đảm bảo tương thích ngược. Tính đến tháng 10 năm 2025, bản phát hành hiện tại là I2P 2.10.0 với Router API phiên bản 0.9.65.

Tài liệu đặc tả này ban đầu được soạn cho phiên bản 0.9.49 (tháng 2 năm 2021) và vẫn hoàn toàn chính xác đối với phiên bản hiện tại 0.9.65 (I2P 2.10.0) vì hệ thống nguồn cấp đăng ký không có thay đổi nào kể từ khi được triển khai lần đầu trong phiên bản 0.9.26.

## Tài liệu tham khảo

- [Đề xuất 112 (Bản gốc)](/proposals/112-addressbook-subscription-feed-commands/)
- [Đặc tả chính thức](/docs/specs/subscription/)
- [Tài liệu đặt tên I2P](/docs/overview/naming/)
- [Đặc tả cấu trúc chung](/docs/specs/common-structures/)
- [Kho mã nguồn I2P](https://github.com/i2p/i2p.i2p)
- [Kho Gitea của I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Các phát triển liên quan

Mặc dù bản thân hệ thống nguồn cấp đăng ký không thay đổi, những phát triển liên quan sau đây trong hạ tầng đặt tên của I2P có thể đáng quan tâm:

- **Tên Base32 mở rộng** (0.9.40+): Hỗ trợ các địa chỉ base32 dài 56+ ký tự cho leasesets được mã hóa. Không ảnh hưởng đến định dạng nguồn cấp đăng ký.
- **Đăng ký TLD .i2p.alt** (RFC 9476, cuối năm 2023): Đăng ký chính thức với GANA cho .i2p.alt như một TLD thay thế. Trong tương lai, các bản cập nhật router có thể loại bỏ hậu tố .alt, nhưng không cần thay đổi các lệnh đăng ký.
- **Mật mã hậu lượng tử** (2.10.0+): Có sẵn nhưng không phải mặc định. Sẽ cân nhắc trong tương lai đối với các thuật toán chữ ký trong nguồn cấp đăng ký.
