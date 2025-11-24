---
title: "Các Lệnh Nguồn Cung Cấp Đăng Ký Danh Bạ"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Đã Đóng"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Ghi chú
Triển khai mạng đã hoàn thành.
Xem [SPEC](/docs/specs/subscription/) để biết đặc tả chính thức.

## Tổng quan

Đề xuất này liên quan đến việc mở rộng nguồn cung cấp đăng ký địa chỉ với các lệnh, để cho phép các máy chủ tên phát sóng cập nhật mục nhập từ người sở hữu tên máy. Được triển khai trong 0.9.26.

## Động lực

Hiện tại, các máy chủ đăng ký hosts.txt chỉ gửi dữ liệu ở định dạng hosts.txt, như sau:

    ```text
    example.i2p=b64destination
    ```

Có một số vấn đề với điều này:

- Người sở hữu tên máy không thể cập nhật Đích liên quan đến tên máy của họ (để ví dụ nâng cấp khóa ký sang loại mạnh hơn).
- Người sở hữu tên máy không thể từ bỏ tên máy của họ tùy ý; họ phải đưa chìa khóa riêng Đích liên quan trực tiếp cho người sở hữu mới.
- Không có cách nào để xác thực rằng một tên miền phụ được kiểm soát bởi tên máy cơ sở tương ứng; điều này hiện chỉ được thực thi riêng bởi một số máy chủ tên.

## Thiết kế

Đề xuất này thêm một số dòng lệnh vào định dạng hosts.txt. Với các lệnh này, các máy chủ tên có thể mở rộng dịch vụ của họ để cung cấp một số tính năng bổ sung. Các khách hàng triển khai đề xuất này sẽ có thể lắng nghe các tính năng này thông qua quy trình đăng ký thông thường.

Tất cả các dòng lệnh phải được ký bởi Đích tương ứng. Điều này đảm bảo rằng các thay đổi chỉ được thực hiện theo yêu cầu của người sở hữu tên máy.

## Tác động bảo mật

Đề xuất này không có tác động đến tính ẩn danh.

Có sự gia tăng rủi ro liên quan đến việc mất quyền kiểm soát một chìa khóa Đích, vì ai đó sở hữu nó có thể sử dụng các lệnh này để thay đổi bất kỳ tên máy liên quan nào. Nhưng điều này không phải là vấn đề hơn so với tình trạng hiện tại, nơi mà ai đó sở hữu một Đích có thể giả mạo một tên máy và (một phần) tiếp quản lưu lượng của nó. Rủi ro gia tăng cũng được cân bằng bởi việc cho phép người sở hữu tên máy có khả năng thay đổi Đích liên quan đến tên máy nếu họ tin rằng Đích đã bị xâm phạm; điều này không thể với hệ thống hiện tại.

## Đặc tả

### Các loại dòng mới

Đề xuất này thêm hai loại dòng mới:

1. Các lệnh Thêm và Thay đổi:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. Các lệnh Xóa:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### Thứ tự
Một nguồn cấp dữ liệu không nhất thiết phải theo thứ tự hoặc hoàn chỉnh. Ví dụ, một lệnh thay đổi có thể nằm trên một dòng trước lệnh thêm, hoặc không có lệnh thêm.

Các khóa có thể ở bất kỳ thứ tự nào. Các khóa trùng lặp không được phép. Tất cả các khóa và giá trị là phân biệt chữ hoa chữ thường.

### Các khóa chung

Bắt buộc trong tất cả các lệnh:

sig
  Chữ ký B64, sử dụng khóa ký từ đích

Tham chiếu đến một tên máy thứ hai và/hoặc đích:

oldname
  Một tên máy thứ hai (mới hoặc thay đổi)
olddest
  Một đích b64 thứ hai (mới hoặc thay đổi)
oldsig
  Chữ ký b64 thứ hai, sử dụng khóa ký từ nolddest

Các khóa thông thường khác:

action
  Một lệnh
name
  Tên máy, chỉ có nếu không có trước example.i2p=b64dest
dest
  Đích b64, chỉ có nếu không có trước example.i2p=b64dest
date
  Số giây kể từ thời điểm epoch
expires
  Số giây kể từ thời điểm epoch

### Các lệnh

Tất cả các lệnh ngoại trừ lệnh "Thêm" phải chứa một cặp khóa/giá trị "action=command".

Để tương thích với các khách hàng cũ hơn, hầu hết các lệnh được đi kèm bởi example.i2p=b64dest, như đã nêu dưới đây. Đối với các thay đổi, đây luôn là các giá trị mới. Bất kỳ giá trị cũ nào đều được bao gồm trong phần khóa/giá trị.

Các khóa được liệt kê là bắt buộc. Tất cả các lệnh có thể chứa thêm các mục khóa/giá trị không được định nghĩa ở đây.

#### Thêm tên máy
Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy và đích mới.
action
  KHÔNG được bao gồm, nó được ngụ ý.
sig
  chữ ký

Ví dụ:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Thay đổi tên máy
Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy mới và đích cũ.
action
  changename
oldname
  tên máy cũ, sẽ được thay thế
sig
  chữ ký

Ví dụ:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Thay đổi đích
Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy cũ và đích mới.
action
  changedest
olddest
  đích cũ, sẽ được thay thế
oldsig
  chữ ký sử dụng olddest
sig
  chữ ký

Ví dụ:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Thêm bí danh tên máy
Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy mới (bí danh) và đích cũ.
action
  addname
oldname
  tên máy cũ
sig
  chữ ký

Ví dụ:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Thêm bí danh đích
(Sử dụng để nâng cấp mã hóa)

Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy cũ và đích (thay thế) mới.
action
  adddest
olddest
  đích cũ
oldsig
  chữ ký sử dụng olddest
sig
  chữ ký sử dụng dest

Ví dụ:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Thêm tên miền phụ
Đi kèm trước bởi subdomain.example.i2p=b64dest
  CÓ, đây là tên máy con miền phụ mới và đích.
action
  addsubdomain
oldname
  tên máy cấp cao hơn (example.i2p)
olddest
  đích cấp cao hơn (cho example.i2p)
oldsig
  chữ ký sử dụng olddest
sig
  chữ ký sử dụng dest

Ví dụ:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Cập nhật siêu dữ liệu
Đi kèm trước bởi example.i2p=b64dest
  CÓ, đây là tên máy và đích cũ.
action
  update
sig
  chữ ký

(thêm bất kỳ khóa cập nhật nào tại đây)

Ví dụ:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Xóa tên máy
Đi kèm trước bởi example.i2p=b64dest
  KHÔNG, những cái này được chỉ định trong tùy chọn
action
  remove
name
  tên máy
dest
  đích
sig
  chữ ký

Ví dụ:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Xóa tất cả với đích này
Đi kèm trước bởi example.i2p=b64dest
  KHÔNG, những cái này được chỉ định trong tùy chọn
action
  removeall
name
  tên máy cũ, chỉ mang tính tư vấn
dest
  đích cũ, tất cả với đích này đều bị xóa
sig
  chữ ký

Ví dụ:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

### Chữ ký

Tất cả các lệnh phải chứa một khóa/giá trị chữ ký "sig=b64signature" mà chữ ký cho dữ liệu khác, sử dụng khóa ký đích.

Đối với các lệnh bao gồm đích cũ và mới, cũng phải có một oldsig=b64signature, và có thể oldname, olddest, hoặc cả hai.

Trong lệnh Thêm hoặc Thay đổi, khóa công khai để xác minh nằm trong Đích được thêm hoặc thay đổi.

Trong một số lệnh thêm hoặc chỉnh sửa, có thể có một đích tham chiếu bổ sung, ví dụ khi thêm một bí danh, hoặc thay đổi một đích hoặc tên máy. Trong trường hợp đó, phải có một chữ ký thứ hai được bao gồm và cả hai cần được xác minh. Chữ ký thứ hai là chữ ký "bên trong" và được ký và xác minh đầu tiên (không bao gồm chữ ký "bên ngoài"). Khách hàng nên thực hiện bất kỳ hành động bổ sung cần thiết nào để xác minh và chấp nhận thay đổi.

oldsig luôn là chữ ký "bên trong". Ký và xác minh không có các khóa 'oldsig' hoặc 'sig'. sig luôn là chữ ký "bên ngoài". Ký và xác minh với khóa 'oldsig' có mặt, nhưng không có khóa 'sig'.

#### Đầu vào cho các chữ ký
Để tạo một chuỗi byte tạo hoặc xác thực chữ ký, tuần tự hóa như sau:

- Loại bỏ khóa "sig"
- Nếu xác minh với oldsig, cũng loại bỏ khóa "oldsig"
- Chỉ đối với các lệnh Thêm hoặc Thay đổi,
  xuất example.i2p=b64dest
- Nếu còn khóa nào, xuất "#!"
- Sắp xếp các tùy chọn theo khóa UTF-8, thất bại nếu có khóa trùng lặp
- Đối với từng cặp khóa/giá trị, xuất khóa=giá trị, sau đó (nếu không phải là cặp khóa/giá trị cuối cùng) một '#'

Ghi chú

- Không xuất một dòng mới
- Mã hóa xuất là UTF-8
- Tất cả mã hóa đích và chữ ký bằng Base 64 sử dụng bảng chữ cái I2P
- Khóa và giá trị phân biệt chữ hoa chữ thường
- Tên máy phải ở dạng chữ thường

## Tương thích

Tất cả các dòng mới trong định dạng hosts.txt được triển khai sử dụng các ký tự bình luận dẫn đầu, vì vậy tất cả các phiên bản I2P cũ hơn sẽ diễn giải các lệnh mới là bình luận.

Khi các bộ định tuyến I2P cập nhật theo đặc tả mới, họ sẽ không diễn giải lại các bình luận cũ, mà sẽ bắt đầu lắng nghe các lệnh mới trong các lần truy xuất sau của nguồn cung cấp đăng ký của họ. Vì vậy, điều quan trọng là các máy chủ tên cần tiếp tục các mục lệnh theo một cách nào đó, hoặc kích hoạt hỗ trợ etag để các bộ định tuyến có thể truy xuất tất cả các lệnh đã qua.
