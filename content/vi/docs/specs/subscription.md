---
title: "Lệnh Feed Đăng ký Sổ địa chỉ"
description: "Đặc tả để mở rộng nguồn cấp đăng ký địa chỉ với các lệnh nhằm cho phép name server phát sóng các cập nhật mục từ những người nắm giữ hostname."
slug: "subscription"
aliases:
  - "/vi/docs/specs/subscription-spec"
  - "/vi/docs/specs/subscription-spec/"
category: "Định dạng"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Tổng quan

Đặc tả này mở rộng nguồn cấp dữ liệu đăng ký địa chỉ với các lệnh, để cho phép các name server phát sóng các cập nhật mục từ những người nắm giữ hostname. Được triển khai trong phiên bản 0.9.26, ban đầu được đề xuất trong đề án 112.

## Động lực

Trước đây, các máy chủ đăng ký hosts.txt chỉ gửi dữ liệu theo định dạng hosts.txt, như sau:

```
example.i2p=b64destination
```
Có một số vấn đề với điều này:

- Chủ sở hữu hostname không thể cập nhật Destination liên kết với hostname của họ (ví dụ để nâng cấp signing key lên loại mạnh hơn).
- Chủ sở hữu hostname không thể từ bỏ hostname của họ một cách tùy ý; họ phải trực tiếp trao private key của Destination tương ứng cho chủ sở hữu mới.
- Không có cách nào để xác thực rằng một subdomain được kiểm soát bởi base hostname tương ứng; điều này hiện tại chỉ được thực thi riêng lẻ bởi một số name server.

## Thiết kế

Đặc tả này bổ sung một số dòng lệnh vào định dạng hosts.txt. Với các lệnh này, các máy chủ tên có thể mở rộng dịch vụ của họ để cung cấp một số tính năng bổ sung. Các client triển khai đặc tả này sẽ có thể lắng nghe các tính năng này thông qua quy trình đăng ký thường xuyên.

Tất cả các dòng lệnh phải được ký bởi Destination tương ứng. Điều này đảm bảo rằng các thay đổi chỉ được thực hiện theo yêu cầu của người sở hữu tên máy chủ.

## Tác động Bảo mật

Đặc tả này không ảnh hưởng đến tính ẩn danh.

Có sự gia tăng rủi ro liên quan đến việc mất quyền kiểm soát khóa Destination, vì ai đó có được nó có thể sử dụng các lệnh này để thực hiện thay đổi đối với bất kỳ tên máy chủ liên quan nào. Nhưng điều này không phải là vấn đề lớn hơn so với hiện trạng, nơi mà ai đó có được một Destination có thể mạo danh một tên máy chủ và (một phần) chiếm quyền kiểm soát lưu lượng truy cập của nó. Rủi ro gia tăng này cũng được cân bằng bằng cách trao cho những người sở hữu tên máy chủ khả năng thay đổi Destination được liên kết với một tên máy chủ, trong trường hợp họ tin rằng Destination đã bị xâm phạm; điều này là không thể với hệ thống hiện tại.

## Đặc tả kỹ thuật

### Các Loại Dòng Mới

Có hai loại dòng mới:

1. Lệnh Add và Change:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Lệnh xóa:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Sắp xếp

Một feed không nhất thiết phải theo thứ tự hoặc đầy đủ. Ví dụ, một lệnh thay đổi có thể ở trên một dòng trước lệnh thêm, hoặc không có lệnh thêm.

Các khóa có thể theo thứ tự bất kỳ. Không được phép có khóa trùng lặp. Tất cả các khóa và giá trị đều phân biệt chữ hoa chữ thường.

### Các Khóa Thông Dụng

Bắt buộc trong tất cả các lệnh:

**sig** : Chữ ký B64, sử dụng khóa ký từ đích đến

Tham chiếu đến hostname thứ hai và/hoặc đích đến:

**oldname** : Một hostname thứ hai (mới hoặc đã thay đổi)

**olddest** : Một destination b64 thứ hai (mới hoặc đã thay đổi)

**oldsig** : Một chữ ký b64 thứ hai, sử dụng khóa ký từ olddest

Các khóa phổ biến khác:

**action** : Một lệnh

**name** : Tên máy chủ, chỉ có mặt nếu không được đứng trước bởi `example.i2p=b64dest`

**dest** : Đích b64, chỉ xuất hiện nếu không được đặt trước bởi `example.i2p=b64dest`

**date** : Tính bằng giây kể từ epoch

**expires** : Tính theo giây kể từ epoch

### Lệnh

Tất cả các lệnh ngoại trừ lệnh "Add" phải chứa một cặp key/value `action=command`.

Để tương thích với các client cũ hơn, hầu hết các lệnh đều có tiền tố `example.i2p=b64dest`, như được ghi chú bên dưới. Đối với các thay đổi, đây luôn là các giá trị mới. Bất kỳ giá trị cũ nào đều được bao gồm trong phần key/value.

Các khóa được liệt kê là bắt buộc. Tất cả các lệnh có thể chứa thêm các mục khóa/giá trị không được định nghĩa ở đây.

#### Thêm Hostname

**Được đi trước bởi example.i2p=b64dest** : CÓ, đây là tên host mới và đích đến.

**action** : KHÔNG được bao gồm, nó được hiểu ngầm.

**sig** : chữ ký

Ví dụ:

```
example.i2p=b64dest#!sig=b64sig
```
#### Thay đổi Tên máy chủ

**Preceded by example.i2p=b64dest** : CÓ, đây là tên host mới và destination cũ.

**action** : changename

**oldname** : tên máy chủ cũ, sẽ được thay thế

**sig** : chữ ký

Ví dụ:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Thay đổi Đích đến

**Đứng trước bởi example.i2p=b64dest** : CÓ, đây là tên host cũ và destination mới.

**action** : changedest

**olddest** : dest cũ, sẽ được thay thế

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký

Ví dụ:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Thêm Bí danh Tên máy chủ

**Preceded by example.i2p=b64dest** : CÓ, đây là tên host (bí danh) mới và đích cũ.

**action** : addname

**oldname** : tên máy chủ cũ

**sig** : chữ ký

Ví dụ:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Thêm Bí danh Đích đến

(Được sử dụng để nâng cấp mã hóa)

**Preceded by example.i2p=b64dest** : CÓ, đây là tên host cũ và đích đến mới (thay thế).

**action** : adddest

**olddest** : dest cũ

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký sử dụng dest

Ví dụ:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Thêm Subdomain

**Preceded by subdomain.example.i2p=b64dest** : CÓ, đây là tên subdomain host mới và destination.

**action** : addsubdomain

**oldname** : tên máy chủ cấp cao hơn (example.i2p)

**olddest** : đích đến cấp cao hơn (ví dụ example.i2p)

**oldsig** : chữ ký sử dụng olddest

**sig** : chữ ký sử dụng dest

Ví dụ:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Cập Nhật Metadata

**Preceded by example.i2p=b64dest** : CÓ, đây là tên host cũ và destination.

**action** : update

**sig** : chữ ký

(thêm bất kỳ khóa cập nhật nào ở đây)

Ví dụ:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Xóa Tên Máy Chủ

**Được đứng trước bởi example.i2p=b64dest** : KHÔNG, những thứ này được chỉ định trong các tùy chọn

**action** : remove

**name** : tên máy chủ

**dest** : điểm đích

**sig** : chữ ký

Ví dụ:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Xóa Tất Cả với Đích Này

**Đứng trước bởi example.i2p=b64dest** : KHÔNG, những thông số này được chỉ định trong các tùy chọn

**action** : removeall

**name** : hostname cũ, chỉ mang tính tham khảo

**dest** : dest cũ, tất cả với dest này sẽ bị xóa

**sig** : chữ ký

Ví dụ:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Chữ ký

Tất cả các lệnh phải chứa cặp khóa/giá trị chữ ký `sig=b64signature` trong đó chữ ký dành cho dữ liệu khác, sử dụng khóa ký của destination.

Đối với các lệnh bao gồm một destination cũ và mới, cũng phải có `oldsig=b64signature`, và oldname, olddest, hoặc cả hai.

Trong lệnh Add hoặc Change, khóa công khai để xác minh nằm trong Destination sẽ được thêm hoặc thay đổi.

Trong một số lệnh thêm hoặc chỉnh sửa, có thể có một destination bổ sung được tham chiếu, ví dụ như khi thêm một bí danh, hoặc thay đổi một destination hoặc tên host. Trong trường hợp đó, phải có một chữ ký thứ hai được bao gồm và cả hai đều phải được xác minh. Chữ ký thứ hai là chữ ký "bên trong" và được ký và xác minh trước (loại trừ chữ ký "bên ngoài"). Client nên thực hiện bất kỳ hành động bổ sung nào cần thiết để xác minh và chấp nhận các thay đổi.

oldsig luôn là chữ ký "bên trong". Ký và xác minh mà không có các khóa 'oldsig' hoặc 'sig' hiện diện. sig luôn là chữ ký "bên ngoài". Ký và xác minh với khóa 'oldsig' có mặt nhưng không có khóa 'sig'.

#### Đầu vào cho Chữ ký

Để tạo một luồng byte để tạo hoặc xác minh chữ ký, hãy tuần tự hóa như sau:

- Xóa khóa "sig"
- Nếu xác minh với oldsig, cũng xóa khóa "oldsig"
- Chỉ đối với các lệnh Add hoặc Change, xuất ra `example.i2p=b64dest`
- Nếu còn lại bất kỳ khóa nào, xuất ra `#!`
- Sắp xếp các tùy chọn theo khóa UTF-8, báo lỗi nếu có khóa trùng lặp
- Đối với mỗi cặp khóa/giá trị, xuất ra `key=value`, sau đó là (nếu không phải cặp khóa/giá trị cuối cùng) một `#`

Ghi chú:

- Không xuất ra ký tự xuống dòng
- Mã hóa đầu ra là UTF-8
- Tất cả mã hóa đích và chữ ký đều ở dạng Base 64 sử dụng bảng chữ cái I2P
- Các khóa và giá trị phân biệt chữ hoa chữ thường
- Tên host phải ở dạng chữ thường

## Khả năng tương thích

Tất cả các dòng mới trong định dạng hosts.txt được triển khai bằng cách sử dụng các ký tự comment đầu dòng, do đó tất cả các phiên bản I2P cũ sẽ hiểu các lệnh mới như là comment.

Khi các I2P router cập nhật lên thông số kỹ thuật mới, chúng sẽ không diễn giải lại các bình luận cũ, nhưng sẽ bắt đầu lắng nghe các lệnh mới trong các lần tải tiếp theo của nguồn cấp dữ liệu đăng ký. Do đó, điều quan trọng là các máy chủ tên phải duy trì các mục lệnh theo cách nào đó, hoặc kích hoạt hỗ trợ etag để các router có thể tải tất cả các lệnh trong quá khứ.
