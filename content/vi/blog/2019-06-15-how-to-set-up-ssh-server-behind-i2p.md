---
title: "Cách thiết lập máy chủ SSH đằng sau I2P để truy cập cá nhân"
date: 2019-06-15
author: "idk"
description: "SSH qua I2P"
---

# Cách thiết lập máy chủ SSH phía sau I2P để truy cập cá nhân

Đây là hướng dẫn về cách thiết lập và tinh chỉnh một tunnel I2P để sử dụng nó nhằm truy cập từ xa vào máy chủ SSH, bằng I2P hoặc i2pd. Hiện tại, hướng dẫn giả định rằng bạn sẽ cài đặt máy chủ SSH của mình từ một trình quản lý gói và rằng nó đang chạy như một dịch vụ.

Các lưu ý: Trong hướng dẫn này, tôi giả định một vài điều. Chúng sẽ cần được điều chỉnh tùy theo những phức tạp nảy sinh trong thiết lập cụ thể của bạn, đặc biệt nếu bạn sử dụng VM (máy ảo) hoặc containers (container) để cô lập. Điều này giả định rằng I2P router và máy chủ SSH đang chạy trên cùng một localhost. Bạn nên sử dụng các khóa máy chủ SSH mới được tạo, hoặc bằng cách dùng một sshd mới cài đặt, hoặc bằng cách xóa các khóa cũ và buộc tạo lại. Ví dụ:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Sử dụng giao diện web của java I2P, truy cập [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) và bắt đầu trình hướng dẫn tunnel (đường hầm).

#### Tunnel Wizard

Vì bạn đang thiết lập tunnel này cho máy chủ SSH, bạn cần chọn loại tunnel "Server".

**Chỗ trống cho ảnh chụp màn hình:** Sử dụng trình hướng dẫn để tạo tunnel "Server"

Bạn nên tinh chỉnh nó sau, nhưng loại tunnel Standard là dễ nhất để bắt đầu.

**Khung giữ chỗ ảnh chụp màn hình:** Thuộc dạng "Standard"

Hãy mô tả nó thật rõ ràng:

**Phần giữ chỗ ảnh chụp màn hình:** Hãy mô tả mục đích của nó

Và cho nó biết máy chủ SSH sẽ khả dụng ở đâu.

**Phần giữ chỗ ảnh chụp màn hình:** Trỏ nó tới vị trí dự định đặt máy chủ SSH của bạn

Xem lại kết quả và lưu cài đặt của bạn.

**Giữ chỗ ảnh chụp màn hình:** Lưu cài đặt.

#### Advanced Settings

Bây giờ hãy quay lại Hidden Services Manager (Trình quản lý Dịch vụ Ẩn) và xem qua các cài đặt nâng cao hiện có. Một điều bạn chắc chắn sẽ muốn thay đổi là thiết lập để dùng kết nối tương tác (interactive connections) thay vì kết nối khối lượng lớn (bulk connections).

**Phần giữ chỗ ảnh chụp màn hình:** Cấu hình tunnel của bạn cho các kết nối tương tác

Ngoài ra, các tùy chọn khác này có thể ảnh hưởng đến hiệu năng khi truy cập máy chủ SSH của bạn. Nếu bạn không quá quan tâm đến tính ẩn danh của mình, bạn có thể giảm số hop bạn sử dụng. Nếu bạn gặp vấn đề về tốc độ, một số lượng tunnel (đường hầm) cao hơn có thể giúp. Một vài tunnel dự phòng có lẽ là một ý tưởng hay. Bạn có thể sẽ phải tinh chỉnh một chút.

**Phần giữ chỗ ảnh chụp màn hình:** Nếu bạn không quan tâm đến tính ẩn danh, thì hãy giảm độ dài tunnel.

Cuối cùng, hãy khởi động lại tunnel để tất cả các cài đặt của bạn có hiệu lực.

Một cài đặt thú vị khác, đặc biệt nếu bạn chọn chạy số lượng tunnels lớn, là "Reduce on Idle", tùy chọn này sẽ giảm số lượng tunnels đang chạy khi serve đã trải qua thời gian dài không hoạt động.

**Phần giữ chỗ ảnh chụp màn hình:** Giảm khi nhàn rỗi, nếu bạn đã chọn số lượng tunnel lớn

### Using i2pd

Với i2pd, mọi cấu hình được thực hiện bằng các tệp thay vì thông qua một giao diện web. Để cấu hình một tunnel dịch vụ SSH cho i2pd, hãy điều chỉnh các thiết lập mẫu sau cho phù hợp với nhu cầu về ẩn danh và hiệu năng của bạn và sao chép chúng vào tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Bước Một: Thiết lập I2P tunnel cho máy chủ SSH

Tùy vào cách bạn muốn truy cập máy chủ SSH của mình, bạn có thể sẽ muốn thay đổi một vài cài đặt. Ngoài những biện pháp tăng cường bảo mật SSH hiển nhiên mà bạn nên áp dụng trên mọi máy chủ SSH (xác thực khóa công khai, không cho phép đăng nhập bằng root, v.v.), nếu bạn không muốn máy chủ SSH lắng nghe trên bất kỳ địa chỉ nào ngoài tunnel máy chủ của bạn, bạn nên đặt AddressFamily thành inet và ListenAddress thành 127.0.0.1.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Nếu bạn chọn sử dụng một cổng khác số 22 cho máy chủ SSH của mình, bạn sẽ cần thay đổi cổng trong cấu hình tunnel I2P của mình.

## Step Three: Set up I2P tunnel for SSH Client

Bạn sẽ cần có thể truy cập bảng điều khiển router I2P của máy chủ SSH để cấu hình kết nối máy khách của bạn. Một điểm hay của thiết lập này là kết nối ban đầu tới I2P tunnel được xác thực, phần nào giảm rủi ro kết nối ban đầu của bạn tới máy chủ SSH bị MITM (Man‑in‑the‑Middle), vốn là một rủi ro trong các kịch bản Trust-On-First-Use (tin cậy khi sử dụng lần đầu).

### Sử dụng I2P phiên bản Java

#### Trình hướng dẫn Tunnel

Trước hết, hãy khởi chạy trình hướng dẫn cấu hình tunnel từ Hidden Services Manager (trình quản lý dịch vụ ẩn) và chọn một client tunnel.

**Phần giữ chỗ ảnh chụp màn hình:** Sử dụng trình hướng dẫn để tạo tunnel máy khách

Tiếp theo, chọn loại tunnel tiêu chuẩn.

Bạn sẽ tinh chỉnh cấu hình này sau.

**Phần giữ chỗ ảnh chụp màn hình:** Loại tiêu chuẩn

Hãy viết một mô tả thật tốt.

**Phần giữ chỗ ảnh chụp màn hình:** Hãy thêm một mô tả thật rõ ràng

Đây là phần duy nhất hơi rắc rối. Hãy truy cập vào trình quản lý dịch vụ ẩn của bảng điều khiển I2P router và tìm "local destination" dạng base64 của tunnel máy chủ SSH. Bạn sẽ cần tìm cách sao chép thông tin này sang bước tiếp theo. Tôi thường tự gửi nó cho mình qua [Tox](https://tox.chat); bất kỳ phương thức off-the-record (không ghi lại) nào cũng đủ đối với hầu hết mọi người.

**Phần giữ chỗ ảnh chụp màn hình:** Tìm destination (đích đến) mà bạn muốn kết nối tới

Sau khi bạn đã tìm thấy đích base64 mà bạn muốn kết nối (được truyền tới thiết bị khách của bạn), hãy dán nó vào trường client destination.

**Giữ chỗ ảnh chụp màn hình:** Cố định điểm đến

Cuối cùng, hãy thiết lập một cổng cục bộ để máy khách SSH của bạn kết nối đến. Cổng cục bộ này sẽ được kết nối tới base64 destination (địa chỉ đích Base64 của I2P), và do đó tới máy chủ SSH.

**Phần giữ chỗ ảnh chụp màn hình:** Chọn một cổng cục bộ

Quyết định liệu bạn có muốn nó khởi động tự động hay không.

**Khung giữ chỗ ảnh chụp màn hình:** Quyết định xem bạn có muốn nó tự khởi động hay không

#### Cài đặt nâng cao

Giống như trước, bạn sẽ muốn thay đổi các cài đặt để tối ưu cho các kết nối tương tác. Ngoài ra, nếu bạn muốn thiết lập danh sách cho phép (whitelist) cho client trên máy chủ, bạn nên chọn nút tùy chọn (radio) "Generate key to enable persistent client tunnel identity".

**Phần giữ chỗ ảnh chụp màn hình:** Cấu hình để nó có thể tương tác

### Using i2pd

Bạn có thể thiết lập điều này bằng cách thêm các dòng sau vào tệp tunnels.conf của bạn và điều chỉnh cho phù hợp với nhu cầu về hiệu năng/ẩn danh của bạn.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Có rất nhiều cách để thiết lập máy khách SSH để kết nối tới máy chủ của bạn trên I2P, nhưng có một vài việc bạn nên làm để bảo mật máy khách SSH của mình cho việc sử dụng ẩn danh. Trước hết, bạn nên cấu hình để nó chỉ tự nhận diện với máy chủ SSH bằng một khóa duy nhất, cụ thể, để tránh nguy cơ làm lộ mối liên hệ giữa các kết nối SSH ẩn danh và không ẩn danh của bạn.

Hãy đảm bảo rằng tệp $HOME/.ssh/config của bạn chứa các dòng sau:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Ngoài ra, bạn có thể thêm một mục trong .bash_alias để buộc áp dụng các tùy chọn của mình và tự động kết nối tới I2P. Bạn hiểu ý rồi, bạn cần buộc áp dụng IdentitiesOnly và cung cấp một tệp khóa danh tính (identity file).

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Điều này gần như là tùy chọn, nhưng khá hay và sẽ ngăn bất kỳ ai tình cờ bắt gặp destination (điểm đích) của bạn khỏi việc có thể nhận ra rằng bạn đang chạy một dịch vụ SSH.

Trước tiên, truy xuất Destination (địa chỉ đích) cố định của client tunnel và truyền nó đến máy chủ.

**Phần giữ chỗ ảnh chụp màn hình:** Lấy điểm đích của máy khách

Thêm destination (đích) base64 của máy khách vào danh sách trắng destination của máy chủ. Từ giờ, bạn chỉ có thể kết nối tới server tunnel từ client tunnel cụ thể đó, và không ai khác có thể kết nối tới destination đó.

**Screenshot placeholder:** And paste it onto the server whitelist

Xác thực lẫn nhau là số một.

**Lưu ý:** Các hình ảnh được tham chiếu trong bài đăng gốc cần được thêm vào thư mục `/static/images/`: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
