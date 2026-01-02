---
title: "Hướng dẫn khắc phục sự cố cho I2P Router"
description: "Hướng dẫn khắc phục sự cố toàn diện cho các vấn đề thường gặp của I2P router, bao gồm các vấn đề về kết nối, hiệu năng và cấu hình"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Các router I2P thường gặp lỗi nhất là do **sự cố chuyển tiếp cổng**, **phân bổ băng thông không đủ**, và **thời gian bootstrap (khởi tạo ban đầu) không đủ**. Ba yếu tố này chiếm hơn 70% các sự cố được báo cáo. Router cần ít nhất **10-15 phút** sau khi khởi động để tích hợp hoàn toàn vào mạng, **băng thông tối thiểu 128 KB/sec** (khuyến nghị 256 KB/sec), và **chuyển tiếp cổng UDP/TCP** đúng cách để đạt trạng thái không bị tường lửa chặn. Người dùng mới thường kỳ vọng kết nối ngay lập tức và khởi động lại quá sớm, điều này đặt lại tiến trình tích hợp và tạo ra một vòng lặp gây khó chịu. Hướng dẫn này cung cấp các giải pháp chi tiết cho mọi vấn đề chính của I2P ảnh hưởng đến các phiên bản 2.10.0 trở lên.

Kiến trúc ẩn danh của I2P vốn dĩ đánh đổi tốc độ để lấy quyền riêng tư thông qua cơ chế tunnel mã hóa đa bước nhảy. Việc hiểu rõ thiết kế nền tảng này giúp người dùng đặt kỳ vọng thực tế và khắc phục sự cố hiệu quả, thay vì hiểu nhầm hành vi bình thường là vấn đề.

## Router không khởi động hoặc bị sập ngay lập tức

Những sự cố khởi động thường gặp nhất xuất phát từ **xung đột cổng**, **không tương thích phiên bản Java**, hoặc **tệp cấu hình bị hỏng**. Hãy kiểm tra xem có tiến trình I2P khác đang chạy hay không trước khi điều tra các vấn đề sâu hơn.

**Xác minh không có tiến trình xung đột:**

Linux: `ps aux | grep i2p` hoặc `netstat -tulpn | grep 7657`

Windows: Trình quản lý tác vụ → Chi tiết → tìm java.exe có i2p trong dòng lệnh

macOS: Activity Monitor → tìm kiếm "i2p"

Nếu có một tiến trình zombie, hãy kết thúc nó: `pkill -9 -f i2p` (Linux/Mac) hoặc `taskkill /F /IM javaw.exe` (Windows)

**Kiểm tra khả năng tương thích phiên bản Java:**

I2P 2.10.0+ yêu cầu **Java 8 tối thiểu**, khuyến nghị Java 11 hoặc mới hơn. Hãy xác minh rằng cài đặt của bạn hiển thị "mixed mode" (chế độ hỗn hợp) (không phải "interpreted mode" (chế độ thông dịch)):

```bash
java -version
```
Nên hiển thị: OpenJDK hoặc Oracle Java, phiên bản 8+, "mixed mode"

**Tránh:** GNU GCJ, các triển khai Java lỗi thời, các chế độ chỉ thông dịch

**Các xung đột cổng thường gặp** xảy ra khi nhiều dịch vụ cùng tranh chấp các cổng mặc định của I2P. Bảng điều khiển router (7657), I2CP (7654), SAM (7656) và proxy HTTP (4444) phải khả dụng. Kiểm tra xung đột: `netstat -ano | findstr "7657 4444 7654"` (Windows) hoặc `lsof -i :7657,4444,7654` (Linux/Mac).

**Hỏng tệp cấu hình** thể hiện bằng việc sập (crash) ngay lập tức với lỗi phân tích cú pháp (parse errors) trong nhật ký. router.config yêu cầu **mã hóa UTF-8 không BOM**, dùng `=` làm ký tự phân tách (không phải `:`), và cấm một số ký tự đặc biệt nhất định. Hãy sao lưu rồi kiểm tra: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Để đặt lại cấu hình mà vẫn giữ nguyên danh tính: Dừng I2P, sao lưu router.keys và thư mục keyData, xóa router.config, rồi khởi động lại I2P. router sẽ tạo lại cấu hình mặc định.

**Phân bổ heap Java quá thấp** gây sập với lỗi OutOfMemoryError. Chỉnh sửa wrapper.config và tăng `wrapper.java.maxmemory` từ mặc định 128 hoặc 256 lên **tối thiểu 512** (1024 cho các router băng thông cao). Việc này yêu cầu tắt hoàn toàn, chờ 11 phút, rồi khởi động lại - nhấp "Restart" trong bảng điều khiển sẽ không áp dụng thay đổi.

## Khắc phục trạng thái "Network: Firewalled"

Trạng thái bị tường lửa chặn nghĩa là router không thể nhận các kết nối vào trực tiếp, buộc phải phụ thuộc vào introducers (các nút trung gian hỗ trợ giới thiệu kết nối). Dù router vẫn hoạt động ở trạng thái này, **hiệu năng giảm sút đáng kể** và mức đóng góp cho mạng vẫn ở mức tối thiểu. Để đạt trạng thái không bị tường lửa chặn, cần cấu hình chuyển tiếp cổng đúng cách.

**router sẽ chọn ngẫu nhiên một cổng** trong khoảng 9000-31000 cho giao tiếp. Hãy xem cổng của bạn tại http://127.0.0.1:7657/confignet - hãy tìm "UDP Port" và "TCP Port" (thường là cùng một số). Bạn phải chuyển tiếp cổng (port forwarding) cho **cả UDP và TCP** để đạt hiệu năng tối ưu, dù chỉ riêng UDP cũng cho phép chức năng cơ bản.

**Bật chuyển tiếp tự động qua UPnP** (cách đơn giản nhất):

1. Truy cập http://127.0.0.1:7657/confignet
2. Chọn "Enable UPnP"
3. Lưu thay đổi và khởi động lại router
4. Chờ 5-10 phút và kiểm tra trạng thái thay đổi từ "Network: Firewalled" sang "Network: OK"

UPnP yêu cầu hỗ trợ từ router (được bật theo mặc định trên hầu hết các router dành cho người tiêu dùng sản xuất sau năm 2010) và cấu hình mạng đúng cách.

**Chuyển tiếp cổng thủ công** (bắt buộc khi UPnP không hoạt động):

1. Ghi lại cổng I2P của bạn từ http://127.0.0.1:7657/confignet (ví dụ: 22648)
2. Tìm địa chỉ IP cục bộ của bạn: `ipconfig` (Windows), `ip addr` (Linux), System Preferences → Network (macOS)
3. Truy cập giao diện quản trị của router (thường là 192.168.1.1 hoặc 192.168.0.1)
4. Đi tới Port Forwarding (có thể nằm dưới Advanced, NAT, hoặc Virtual Servers)
5. Tạo hai quy tắc:
   - Cổng ngoài: [cổng I2P của bạn] → IP nội bộ: [máy tính của bạn] → Cổng nội bộ: [giữ nguyên] → Giao thức: **UDP**
   - Cổng ngoài: [cổng I2P của bạn] → IP nội bộ: [máy tính của bạn] → Cổng nội bộ: [giữ nguyên] → Giao thức: **TCP**
6. Lưu cấu hình và khởi động lại router nếu cần

**Xác minh chuyển tiếp cổng** bằng các công cụ kiểm tra trực tuyến sau khi cấu hình. Nếu không phát hiện được, hãy kiểm tra cài đặt tường lửa - cả tường lửa hệ thống và tường lửa của bất kỳ phần mềm chống virus nào cũng phải cho phép cổng I2P.

**Phương án thay thế bằng chế độ ẩn (Hidden mode)** cho các mạng bị hạn chế nơi việc chuyển tiếp cổng là không thể: Bật tại http://127.0.0.1:7657/confignet → chọn "Hidden mode". The router vẫn bị tường lửa chặn nhưng tối ưu cho trạng thái này bằng cách chỉ sử dụng SSU introducers (nút trung gian giới thiệu). Hiệu năng sẽ chậm hơn nhưng vẫn hoạt động.

## Router bị kẹt ở trạng thái "Starting" hoặc "Testing"

Những trạng thái tạm thời trong giai đoạn khởi tạo ban đầu thường tự ổn định trong vòng **10-15 phút đối với các cài đặt mới** hoặc **3-5 phút đối với các router đã hoạt động**. Việc can thiệp quá sớm thường khiến vấn đề trở nên trầm trọng hơn.

**"Network: Testing"** cho biết router đang thăm dò khả năng được kết nối từ bên ngoài qua nhiều kiểu kết nối (kết nối trực tiếp, introducers (các nút giới thiệu hỗ trợ kết nối qua NAT), nhiều phiên bản giao thức). Đây là điều **bình thường trong 5–10 phút đầu** sau khi khởi động. Router kiểm tra nhiều kịch bản để xác định cấu hình tối ưu.

**"Rejecting tunnels: starting up"** xuất hiện trong giai đoạn bootstrap (khởi động ban đầu) khi router chưa có đủ thông tin về các nút ngang hàng. Router sẽ không tham gia chuyển tiếp lưu lượng cho đến khi được tích hợp đầy đủ vào mạng. Thông điệp này sẽ biến mất sau 10-20 phút khi netDb đã có dữ liệu về hơn 50 router.

**Sai lệch đồng hồ phá hỏng việc kiểm tra khả năng kết nối.** I2P yêu cầu thời gian hệ thống nằm trong **±60 giây** so với thời gian mạng. Chênh lệch vượt quá 90 giây sẽ khiến kết nối bị tự động từ chối. Đồng bộ đồng hồ hệ thống của bạn:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Bảng điều khiển → Ngày và Giờ → Thời gian Internet → Cập nhật ngay → Bật đồng bộ tự động

macOS: Tùy chọn Hệ thống → Ngày & Giờ → Bật "Đặt ngày và giờ tự động"

Sau khi khắc phục clock skew (sai lệch thời gian của đồng hồ hệ thống), hãy khởi động lại I2P hoàn toàn để tích hợp đúng cách.

**Phân bổ băng thông không đủ** ngăn cản việc thử nghiệm thành công. router cần đủ băng thông để xây dựng các tunnel thử nghiệm. Cấu hình tại http://127.0.0.1:7657/config:

- **Tối thiểu đủ dùng:** Vào 96 KB/giây, Ra 64 KB/giây
- **Khuyến nghị (chuẩn):** Vào 256 KB/giây, Ra 128 KB/giây  
- **Hiệu suất tối ưu:** Vào 512+ KB/giây, Ra 256+ KB/giây
- **Tỷ lệ chia sẻ:** 80% (cho phép router đóng góp băng thông cho mạng)

Băng thông thấp hơn có thể vẫn hoạt động nhưng sẽ kéo dài thời gian tích hợp từ vài phút lên hàng giờ.

**netDb bị hỏng** do tắt máy không đúng cách hoặc lỗi ổ đĩa gây ra các vòng lặp kiểm thử liên tục. Router không thể hoàn tất kiểm thử nếu không có dữ liệu peer hợp lệ:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Xóa nội dung của `%APPDATA%\I2P\netDb\` hoặc `%LOCALAPPDATA%\I2P\netDb\`

**Tường lửa chặn reseed (tải về thông tin router ban đầu)** khiến không thể thu nhận các nút ban đầu. Trong giai đoạn khởi tạo, I2P tải về thông tin router từ các máy chủ reseed qua HTTPS. Tường lửa của doanh nghiệp/ISP có thể chặn các kết nối này. Hãy cấu hình proxy reseed tại http://127.0.0.1:7657/configreseed nếu hoạt động phía sau các mạng bị hạn chế.

## Tốc độ chậm, hết thời gian chờ, và lỗi xây dựng tunnel

Thiết kế của I2P vốn dĩ dẫn đến **tốc độ chậm hơn 3–10 lần so với clearnet (mạng công khai)** do mã hóa đa hop, overhead gói tin và tính khó đoán của đường đi. Quá trình xây dựng tunnel đi qua nhiều router, mỗi router đều thêm độ trễ. Hiểu điều này giúp tránh chẩn đoán nhầm hành vi bình thường thành sự cố.

**Kỳ vọng hiệu năng điển hình:**

- Duyệt web các trang .i2p: ban đầu tải trang mất 10-30 giây, nhanh hơn sau khi thiết lập tunnel
- Tải torrent qua I2PSnark: 10-100 KB/giây cho mỗi torrent tùy theo người seed (seeders) và điều kiện mạng  
- Tải xuống tệp lớn: Cần kiên nhẫn - tệp cỡ megabyte có thể mất vài phút, gigabyte mất hàng giờ
- Kết nối đầu tiên chậm nhất: Việc xây dựng tunnel mất 30-90 giây; các kết nối tiếp theo dùng các tunnel hiện có

**Tỷ lệ thành công khi xây dựng Tunnel** cho biết tình trạng sức khỏe của mạng. Kiểm tra tại http://127.0.0.1:7657/tunnels:

- **Trên 60%:** Bình thường, hoạt động ổn định
- **40-60%:** Cận biên, cân nhắc tăng băng thông hoặc giảm tải
- **Dưới 40%:** Có vấn đề - cho thấy băng thông không đủ, sự cố mạng, hoặc lựa chọn nút ngang hàng kém

**Tăng phân bổ băng thông** là bước tối ưu hóa đầu tiên. Tình trạng chậm chạp phần lớn xuất phát từ việc thiếu băng thông. Tại http://127.0.0.1:7657/config, hãy tăng dần các giới hạn và theo dõi biểu đồ tại http://127.0.0.1:7657/graphs.

**Dành cho DSL/Cable (kết nối 1-10 Mbps):** - Băng thông vào: 400 KB/giây - Băng thông ra: 200 KB/giây - Chia sẻ: 80% - Bộ nhớ: 384 MB (chỉnh sửa wrapper.config)

**Đối với kết nối tốc độ cao (10-100+ Mbps):** - Vào: 1500 KB/giây   - Ra: 1000 KB/giây - Chia sẻ: 80-100% - Bộ nhớ: 512-1024 MB - Cân nhắc: Tăng số lượng tunnels tham gia lên 2000-5000 tại http://127.0.0.1:7657/configadvanced

**Tối ưu cấu hình tunnel** để có hiệu năng tốt hơn. Truy cập các cài đặt tunnel cụ thể tại http://127.0.0.1:7657/i2ptunnel và chỉnh sửa từng tunnel:

- **Số lượng tunnel:** Tăng từ 2 lên 3-4 (có nhiều đường đi hơn)
- **Số lượng dự phòng:** Đặt thành 1-2 (chuyển đổi dự phòng nhanh nếu tunnel gặp sự cố)
- **Độ dài tunnel:** Mặc định 3 hop (chặng) mang lại cân bằng tốt; giảm xuống 2 cải thiện tốc độ nhưng giảm tính ẩn danh

**Thư viện mật mã gốc (jbigi)** cho hiệu năng tốt hơn 5-10x so với mã hóa Java thuần. Xác minh đã được nạp tại http://127.0.0.1:7657/logs - hãy tìm "jbigi loaded successfully" hoặc "Using native CPUID implementation". Nếu không thấy:

Linux: Thông thường được tự động phát hiện và nạp từ ~/.i2p/jbigi-*.so Windows: Kiểm tra jbigi.dll trong thư mục cài đặt I2P Nếu thiếu: Cài đặt các công cụ biên dịch/xây dựng và biên dịch từ mã nguồn, hoặc tải các tệp nhị phân đã biên dịch sẵn từ các kho lưu trữ chính thức

**Giữ router chạy liên tục.** Mỗi lần khởi động lại sẽ đặt lại trạng thái hòa nhập, cần 30-60 phút để xây dựng lại mạng lưới tunnel và các mối quan hệ với các nút (peer). Các router ổn định với thời gian hoạt động (uptime) cao sẽ được ưu tiên chọn khi xây dựng tunnel, tạo ra vòng phản hồi tích cực cho hiệu năng.

## Mức sử dụng CPU và bộ nhớ cao

Việc sử dụng tài nguyên quá mức thường cho thấy **cấp phát bộ nhớ không đầy đủ**, **thiếu các thư viện mật mã gốc (native)**, hoặc **quá mức cam kết với việc tham gia mạng**. Các router được cấu hình tốt nên tiêu thụ 10-30% CPU trong khi hoạt động và duy trì mức sử dụng bộ nhớ ổn định dưới 80% của heap (vùng bộ nhớ heap) được cấp phát.

**Các vấn đề về bộ nhớ biểu hiện như sau:** - Biểu đồ bộ nhớ đỉnh phẳng (bị ghim ở mức tối đa) - Thu gom rác (garbage collection) diễn ra thường xuyên (mẫu răng cưa với các đợt tụt mạnh) - OutOfMemoryError trong nhật ký - Router trở nên không phản hồi khi chịu tải - Tự động tắt do cạn kiệt tài nguyên

**Tăng phân bổ bộ nhớ heap của Java** trong wrapper.config (yêu cầu tắt hoàn toàn):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Quan trọng:** Sau khi chỉnh sửa wrapper.config, bạn **phải tắt hoàn toàn** (không khởi động lại), chờ 11 phút để quá trình kết thúc an toàn, rồi khởi động mới. Nút "Restart" trên Router console không tải lại các thiết lập của wrapper.

**Tối ưu hóa CPU cần thư viện mật mã gốc (native).** Các phép toán BigInteger thuần Java tiêu tốn CPU gấp 10–20 lần so với các triển khai native. Hãy kiểm tra trạng thái jbigi tại http://127.0.0.1:7657/logs trong khi khởi động. Nếu không có jbigi, CPU sẽ tăng vọt lên 50–100% trong quá trình xây dựng tunnel và các hoạt động mã hóa.

**Giảm tải từ các tunnel tham gia** nếu router bị quá tải:

1. Truy cập http://127.0.0.1:7657/configadvanced
2. Thiết lập `router.maxParticipatingTunnels=1000` (mặc định là 8000)
3. Giảm tỷ lệ chia sẻ tại http://127.0.0.1:7657/config từ 80% xuống 50%
4. Tắt chế độ floodfill nếu đang bật: `router.floodfillParticipant=false`

**Giới hạn băng thông và số torrent hoạt động đồng thời của I2PSnark.** Việc tải torrent tiêu tốn đáng kể tài nguyên. Tại http://127.0.0.1:7657/i2psnark:

- Giới hạn số torrent đang hoạt động tối đa 3-5
- Đặt "Up BW Limit" và "Down BW Limit" ở các giá trị hợp lý (50-100 KB/giây mỗi cái)
- Dừng torrent khi không còn cần thiết
- Tránh seed (chia sẻ) hàng chục torrent cùng lúc

**Theo dõi mức sử dụng tài nguyên** thông qua các đồ thị tích hợp sẵn tại http://127.0.0.1:7657/graphs. Bộ nhớ nên thể hiện còn dư địa (headroom), không phải đỉnh phẳng (flat-top). Các đột biến CPU trong lúc xây dựng tunnel là bình thường; CPU cao kéo dài cho thấy có vấn đề về cấu hình.

**Đối với các hệ thống rất hạn chế tài nguyên** (Raspberry Pi, phần cứng cũ), hãy cân nhắc **i2pd** (triển khai C++) như một lựa chọn thay thế. i2pd cần ~130 MB RAM so với 350+ MB của Java I2P, và dùng ~7% CPU so với 70% dưới tải tương tự. Lưu ý rằng i2pd không có ứng dụng tích hợp sẵn và cần các công cụ bên ngoài.

## Các sự cố torrent của I2PSnark

Để I2PSnark tích hợp với kiến trúc router của I2P, cần hiểu rằng **việc torrent phụ thuộc hoàn toàn vào tình trạng hoạt động của tunnel trên router**. Các torrent sẽ không bắt đầu cho đến khi router đạt mức hòa nhập mạng đủ tốt với hơn 10 nút ngang hàng đang hoạt động và các tunnel hoạt động bình thường.

**Các torrent bị kẹt ở mức 0% thường là dấu hiệu cho thấy:**

1. **Router chưa tích hợp đầy đủ:** Chờ 10-15 phút sau khi I2P khởi động trước khi mong đợi có hoạt động torrent
2. **DHT (bảng băm phân tán) bị tắt:** Bật tại http://127.0.0.1:7657/i2psnark → Configuration → đánh dấu "Enable DHT" (mặc định bật từ phiên bản 0.9.2)
3. **Tracker không hợp lệ hoặc đã chết:** Torrent trên I2P yêu cầu tracker dành riêng cho I2P - tracker clearnet (mạng Internet công khai) sẽ không hoạt động
4. **Cấu hình tunnel không đủ:** Tăng số lượng tunnel tại I2PSnark Configuration → phần Tunnels

**Cấu hình I2PSnark tunnels để cải thiện hiệu năng:**

- Tunnel vào: 3-5 (mặc định là 2 cho Java I2P, 5 cho i2pd)
- Tunnel ra: 3-5  
- Độ dài tunnel: 3 hop (bước nhảy qua nút trung gian; giảm xuống 2 để tăng tốc, ít ẩn danh hơn)
- Số lượng tunnel: 3 (cho hiệu năng ổn định)

**Các tracker (máy chủ theo dõi) torrent I2P thiết yếu** cần thêm: - tracker2.postman.i2p (chính, đáng tin cậy nhất) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Hãy loại bỏ mọi tracker clearnet (internet công khai, không phải .i2p) - chúng không mang lại giá trị nào và tạo ra các lần thử kết nối bị hết thời gian chờ.

**Lỗi "Torrent not registered"** xảy ra khi việc giao tiếp với tracker thất bại. Nhấp chuột phải vào torrent → "Start" sẽ buộc thông báo lại với tracker. Nếu vẫn tiếp diễn, hãy kiểm tra khả năng truy cập của tracker bằng cách truy cập http://tracker2.postman.i2p trong trình duyệt đã được cấu hình I2P. Các tracker chết nên được thay bằng các lựa chọn thay thế còn hoạt động.

**Không có peer (nút ngang hàng) nào kết nối** mặc dù tracker phản hồi thành công, có thể do: - Router bị tường lửa chặn (cải thiện khi bật port forwarding (chuyển tiếp cổng) nhưng không bắt buộc) - Băng thông không đủ (tăng lên 256+ KB/sec)   - Swarm (nhóm người dùng chia sẻ) quá nhỏ (một số torrent chỉ có 1-2 seeders (máy chia sẻ); cần kiên nhẫn) - DHT bị tắt (bật để tìm peer không cần tracker)

**Kích hoạt DHT (bảng băm phân tán) và PEX (Peer Exchange - trao đổi nút)** trong I2PSnark Configuration. DHT cho phép tìm các nút mà không phụ thuộc vào tracker (máy theo dõi). PEX khám phá các nút từ các nút đã kết nối, tăng tốc quá trình phát hiện swarm (tập hợp các nút trong torrent).

**Hư hỏng tệp đã tải xuống** hiếm khi xảy ra nhờ cơ chế kiểm tra tính toàn vẹn tích hợp sẵn của I2PSnark. Nếu phát hiện:

1. Nhấp chuột phải vào torrent → "Check" sẽ buộc băm lại tất cả các mảnh
2. Xóa dữ liệu torrent bị hỏng (giữ lại tệp .torrent)  
3. Nhấp chuột phải → "Start" để tải lại kèm xác minh từng mảnh
4. Kiểm tra ổ đĩa để tìm lỗi nếu vẫn còn hỏng: `chkdsk` (Windows), `fsck` (Linux)

**Tính năng theo dõi thư mục không hoạt động** cần được cấu hình đúng cách:

1. Cấu hình I2PSnark → "Watch directory": Đặt đường dẫn tuyệt đối (ví dụ: `/home/user/torrents/watch`)
2. Đảm bảo tiến trình I2P có quyền đọc: `chmod 755 /path/to/watch`
3. Đặt các tệp .torrent vào thư mục Watch directory - I2PSnark sẽ tự động thêm chúng
4. Cấu hình "Auto start": Đánh dấu chọn để các torrent bắt đầu ngay khi được thêm

**Tối ưu hiệu năng cho việc tải torrent:**

- Giới hạn số torrent hoạt động đồng thời: tối đa 3-5 cho các kết nối tiêu chuẩn
- Ưu tiên các tải xuống quan trọng: Dừng tạm thời các torrent ưu tiên thấp
- Tăng phân bổ băng thông cho router: Nhiều băng thông hơn = hiệu suất torrent tốt hơn
- Hãy kiên nhẫn: Tải torrent qua I2P vốn dĩ chậm hơn so với BitTorrent trên clearnet (Internet công khai)
- Seed sau khi tải xong: Mạng lưới phát triển nhờ tính có đi có lại

## Cấu hình và khắc phục sự cố Git qua I2P

Các thao tác Git qua I2P cần hoặc **cấu hình proxy SOCKS** hoặc **I2P tunnels chuyên dụng** để truy cập SSH/HTTP. Thiết kế của Git giả định các kết nối có độ trễ thấp, khiến việc hoạt động qua kiến trúc có độ trễ cao của I2P trở nên thách thức.

**Cấu hình Git để sử dụng proxy SOCKS của I2P:**

Chỉnh sửa ~/.ssh/config (tạo nếu chưa có):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Điều này định tuyến tất cả các kết nối SSH tới các máy chủ .i2p thông qua SOCKS proxy của I2P (cổng 4447). Các thiết lập ServerAlive (tùy chọn giữ kết nối của SSH) duy trì kết nối khi I2P có độ trễ.

Đối với các thao tác git qua HTTP/HTTPS, hãy cấu hình git ở mức toàn cục:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Lưu ý: `socks5h` thực hiện phân giải DNS thông qua proxy - rất quan trọng đối với các tên miền .i2p.

**Tạo I2P tunnel chuyên dụng cho Git SSH** (đáng tin cậy hơn so với SOCKS):

1. Truy cập http://127.0.0.1:7657/i2ptunnel
2. "New client tunnel" → "Standard"
3. Cấu hình:
   - Tên: Git-SSH  
   - Loại: Client
   - Cổng: 2222 (cổng cục bộ để truy cập Git)
   - Đích: [your-git-server].i2p:22
   - Tự động khởi động: Bật
   - Số lượng tunnel: 3-4 (cao hơn để tăng độ tin cậy)
4. Lưu và khởi động tunnel
5. Cấu hình SSH để sử dụng tunnel: `ssh -p 2222 git@127.0.0.1`

**Các lỗi xác thực SSH** qua I2P thường bắt nguồn từ:

- Chưa thêm khóa vào ssh-agent: `ssh-add ~/.ssh/id_rsa`
- Phân quyền tệp khóa không đúng: `chmod 600 ~/.ssh/id_rsa`
- Tunnel không chạy: Xác minh tại http://127.0.0.1:7657/i2ptunnel hiển thị trạng thái màu xanh
- Máy chủ Git yêu cầu loại khóa cụ thể: Tạo khóa ed25519 nếu RSA không thành công

**Các thao tác Git bị hết thời gian chờ** liên quan đến đặc tính độ trễ của I2P:

- Tăng thời gian chờ của Git: `git config --global http.postBuffer 524288000` (bộ đệm 500MB)
- Tăng giới hạn tốc độ thấp: `git config --global http.lowSpeedLimit 1000` và `git config --global http.lowSpeedTime 600` (chờ 10 phút)
- Sử dụng shallow clone (clone nông) cho lần clone ban đầu: `git clone --depth 1 [url]` (chỉ tải commit mới nhất, nhanh hơn)
- Thực hiện clone vào các khoảng thời gian ít hoạt động: Tắc nghẽn mạng ảnh hưởng đến hiệu năng I2P

**Các thao tác git clone/fetch chậm** là đặc tính vốn có của kiến trúc I2P. Một kho mã nguồn 100MB có thể mất 30-60 phút qua I2P, so với chỉ vài giây trên clearnet (mạng công khai). Chiến lược:

- Sử dụng shallow clone (clone nông): `--depth 1` giảm đáng kể lượng dữ liệu truyền ban đầu
- Fetch theo từng phần: Thay vì clone đầy đủ, fetch các nhánh cụ thể: `git fetch origin branch:branch`
- Cân nhắc rsync qua I2P: Với các kho rất lớn, rsync có thể cho hiệu năng tốt hơn
- Tăng số lượng tunnel: Nhiều tunnel mang lại thông lượng tốt hơn cho các truyền tải dữ liệu lớn kéo dài

**Các lỗi "Connection refused"** cho thấy cấu hình tunnel sai:

1. Xác minh I2P router (bộ định tuyến) đang chạy: Kiểm tra http://127.0.0.1:7657
2. Xác nhận tunnel (đường hầm) đang hoạt động và hiển thị màu xanh tại http://127.0.0.1:7657/i2ptunnel
3. Kiểm tra tunnel: `nc -zv 127.0.0.1 2222` (sẽ kết nối nếu tunnel hoạt động)
4. Kiểm tra đích có thể truy cập: Truy cập giao diện HTTP của đích nếu có
5. Xem lại nhật ký tunnel tại http://127.0.0.1:7657/logs để tìm lỗi cụ thể

**Thực tiễn tốt nhất cho Git (hệ thống quản lý phiên bản phân tán) qua I2P:**

- Giữ I2P router chạy liên tục để truy cập Git ổn định
- Sử dụng khóa SSH thay vì xác thực bằng mật khẩu (ít lời nhắc tương tác hơn)
- Cấu hình tunnels thường trực thay vì các kết nối SOCKS tạm thời
- Cân nhắc tự lưu trữ máy chủ git I2P để kiểm soát tốt hơn
- Ghi lại các điểm cuối git .i2p của bạn cho cộng tác viên

## Truy cập các eepsite và phân giải tên miền .i2p

Lý do thường gặp nhất khiến người dùng không thể truy cập các trang .i2p là **cấu hình proxy trình duyệt không đúng**. Các trang I2P chỉ tồn tại trong mạng I2P và cần được định tuyến thông qua proxy HTTP của I2P.

**Thiết lập cài đặt proxy của trình duyệt chính xác như sau:**

**Firefox (được khuyến nghị cho I2P):**

1. Menu → Cài đặt → Cài đặt mạng → nút Cài đặt
2. Chọn "Cấu hình proxy thủ công"
3. Proxy HTTP: **127.0.0.1** Cổng: **4444**
4. Proxy SSL: **127.0.0.1** Cổng: **4444**  
5. Proxy SOCKS: **127.0.0.1** Cổng: **4447** (tùy chọn, dành cho ứng dụng SOCKS)
6. Chọn "Proxy DNS khi dùng SOCKS v5"
7. Nhấn OK để lưu

**Các cài đặt about:config quan trọng của Firefox:**

Truy cập `about:config` và chỉnh sửa:

- `media.peerconnection.ice.proxy_only` = **true** (ngăn rò rỉ địa chỉ IP qua WebRTC)
- `keyword.enabled` = **false** (ngăn địa chỉ .i2p bị chuyển hướng đến công cụ tìm kiếm)
- `network.proxy.socks_remote_dns` = **true** (DNS qua proxy)

**Các hạn chế của Chrome/Chromium:**

Chrome sử dụng cài đặt proxy toàn hệ thống thay vì theo từng ứng dụng. Trên Windows: Cài đặt → tìm kiếm "proxy" → "Mở cài đặt proxy của máy tính" → Cấu hình HTTP: 127.0.0.1:4444 và HTTPS: 127.0.0.1:4445.

Cách tiếp cận tốt hơn: Sử dụng tiện ích mở rộng FoxyProxy hoặc Proxy SwitchyOmega để định tuyến .i2p có chọn lọc.

**Các lỗi "Website Not Found In Address Book"** có nghĩa là router không có địa chỉ mật mã của miền .i2p. I2P sử dụng sổ địa chỉ cục bộ thay vì DNS tập trung. Giải pháp:

**Phương pháp 1: Sử dụng jump services (dịch vụ "jump" giúp truy cập các trang mới chưa có trong sổ địa chỉ)** (dễ nhất cho các trang mới):

Truy cập http://stats.i2p và tìm kiếm trang web. Nhấp vào liên kết addresshelper: `http://example.i2p/?i2paddresshelper=base64destination`. Trình duyệt của bạn sẽ hiển thị "Lưu vào sổ địa chỉ?" - xác nhận để thêm.

**Phương pháp 2: Cập nhật các đăng ký sổ địa chỉ:**

1. Truy cập http://127.0.0.1:7657/dns (SusiDNS)
2. Nhấp vào thẻ "Subscriptions"  
3. Kiểm tra các đăng ký đang hoạt động (mặc định: http://i2p-projekt.i2p/hosts.txt)
4. Thêm các đăng ký được khuyến nghị:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Nhấp "Update Now" để buộc cập nhật đăng ký ngay lập tức
6. Chờ 5-10 phút để xử lý

**Cách 3: Sử dụng địa chỉ base32** (luôn hoạt động nếu trang web đang trực tuyến):

Mỗi site .i2p đều có một địa chỉ Base32: 52 ký tự ngẫu nhiên theo sau là .b32.i2p (ví dụ, `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Các địa chỉ Base32 bỏ qua sổ địa chỉ (addressbook) - router thực hiện tra cứu mật mã trực tiếp.

**Các lỗi cấu hình trình duyệt thường gặp:**

- Cố dùng HTTPS với các trang chỉ hỗ trợ HTTP: Hầu hết các trang .i2p chỉ dùng HTTP - thử `https://example.i2p` sẽ thất bại
- Quên tiền tố `http://`: Trình duyệt có thể tìm kiếm thay vì kết nối - luôn dùng `http://example.i2p`
- WebRTC được bật: Có thể làm lộ địa chỉ IP thật - tắt qua cài đặt Firefox hoặc tiện ích mở rộng
- DNS không qua proxy: DNS clearnet (internet công khai) không thể phân giải .i2p - phải đưa các truy vấn DNS qua proxy
- Sai cổng proxy: 4444 dành cho HTTP (không phải 4445, đây là HTTPS outproxy (proxy đi ra) tới clearnet)

**Router chưa được tích hợp đầy đủ** khiến không thể truy cập bất kỳ trang web nào. Hãy kiểm tra mức độ tích hợp đã đủ:

1. Kiểm tra http://127.0.0.1:7657 hiển thị "Network: OK" hoặc "Network: Firewalled" (không phải "Network: Testing")
2. Mục Active peers hiển thị tối thiểu 10+ (50+ là tối ưu)  
3. Không có thông báo "Rejecting tunnels: starting up"
4. Chờ đủ 10-15 phút sau khi router khởi động trước khi mong đợi truy cập .i2p

**Cấu hình IRC và trình khách email** tuân theo các mẫu proxy tương tự:

**IRC:** Các trình khách kết nối tới **127.0.0.1:6668** (tunnel proxy IRC của I2P). Tắt cài đặt proxy của trình khách IRC - kết nối tới localhost:6668 đã được proxy qua I2P.

**Email (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Không dùng SSL/TLS (mã hóa được xử lý bởi I2P tunnel) - Thông tin đăng nhập từ đăng ký tài khoản trên postman.i2p

Tất cả các tunnels này phải hiển thị trạng thái "running" (màu xanh lá) tại http://127.0.0.1:7657/i2ptunnel.

## Lỗi cài đặt và sự cố gói phần mềm

Các cài đặt dựa trên gói (Debian, Ubuntu, Arch) đôi khi bị lỗi do **thay đổi kho lưu trữ**, **khóa GPG hết hạn**, hoặc **xung đột phụ thuộc**. Các kho chính thức đã chuyển từ deb.i2p2.de/deb.i2p2.no (đã ngừng hỗ trợ) sang **deb.i2p.net** trong các phiên bản gần đây.

**Cập nhật kho phần mềm Debian/Ubuntu lên phiên bản hiện tại:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Các lỗi xác minh chữ ký GPG** xảy ra khi các khóa của kho lưu trữ hết hạn hoặc thay đổi:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**Dịch vụ không khởi động sau khi cài đặt gói** thường là do các sự cố với AppArmor profile trên Debian/Ubuntu:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Vấn đề quyền truy cập** trên I2P được cài đặt từ gói:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Các vấn đề về khả năng tương thích Java:**

I2P 2.10.0 yêu cầu **tối thiểu Java 8**. Các hệ thống cũ hơn có thể có Java 7 hoặc cũ hơn:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Lỗi cấu hình Wrapper** ngăn dịch vụ khởi động:

Vị trí của Wrapper.config thay đổi tùy theo phương pháp cài đặt: - Cài đặt người dùng: `~/.i2p/wrapper.config` - Cài đặt từ gói: `/etc/i2p/wrapper.config` hoặc `/var/lib/i2p/wrapper.config`

Các vấn đề thường gặp với wrapper.config:

- Đường dẫn sai: `wrapper.java.command` phải trỏ tới cài đặt Java hợp lệ
- Không đủ bộ nhớ: `wrapper.java.maxmemory` được đặt quá thấp (tăng lên 512+)
- Sai vị trí pidfile: `wrapper.pidfile` phải là một vị trí có thể ghi
- Thiếu tệp nhị phân của wrapper (trình bao): Một số nền tảng không có wrapper được biên dịch sẵn (sử dụng runplain.sh như phương án dự phòng)

**Các lỗi cập nhật và các bản cập nhật bị hỏng:**

Các bản cập nhật Router console đôi khi thất bại giữa quá trình tải xuống do gián đoạn mạng. Quy trình cập nhật thủ công:

1. Tải xuống i2pupdate_X.X.X.zip từ https://geti2p.net/en/download
2. Xác minh checksum (tổng kiểm tra) SHA256 khớp với hash (giá trị băm) đã công bố
3. Sao chép vào thư mục cài đặt I2P với tên `i2pupdate.zip`
4. Khởi động lại router - tự động phát hiện và giải nén bản cập nhật
5. Chờ 5-10 phút để cài đặt bản cập nhật
6. Kiểm tra phiên bản mới tại http://127.0.0.1:7657

**Nâng cấp từ các phiên bản rất cũ** (trước 0.9.47) lên các phiên bản hiện tại có thể thất bại do khóa ký không tương thích hoặc do các tính năng đã bị loại bỏ. Cần cập nhật theo từng bước:

- Các phiên bản cũ hơn 0.9.9: Không thể xác minh chữ ký số hiện tại - cần cập nhật thủ công
- Các phiên bản chạy trên Java 6/7: Phải nâng cấp Java trước khi cập nhật I2P lên 2.x
- Chênh lệch lớn giữa các phiên bản chính: Hãy cập nhật lên phiên bản trung gian trước (0.9.47 là mốc khuyến nghị)

**Khi nào nên dùng trình cài đặt và khi nào nên dùng gói:**

- **Gói (apt/yum):** Phù hợp nhất cho máy chủ, cập nhật bảo mật tự động, tích hợp hệ thống, quản lý bằng systemd
- **Trình cài đặt (.jar):** Phù hợp nhất cho cài đặt cấp người dùng, Windows, macOS, cài đặt tùy chỉnh, có sẵn phiên bản mới nhất

## Hỏng tệp cấu hình và khôi phục

Việc lưu trạng thái cấu hình của I2P dựa vào một số tệp quan trọng. Hỏng tệp thường xuất phát từ **tắt không đúng cách**, **lỗi đĩa**, hoặc **sai sót khi chỉnh sửa thủ công**. Hiểu rõ mục đích của từng tệp cho phép tiến hành sửa chữa chính xác thay vì phải cài đặt lại toàn bộ.

**Các tệp quan trọng và mục đích của chúng:**

- **router.keys** (516+ bytes): Danh tính mật mã của router - mất sẽ tạo danh tính mới
- **router.info** (tự động tạo): Thông tin router được công bố - có thể xóa an toàn, sẽ được tạo lại  
- **router.config** (văn bản): Cấu hình chính - băng thông, cài đặt mạng, tùy chọn
- **i2ptunnel.config** (văn bản): Định nghĩa tunnel - các tunnel máy khách/máy chủ, khóa, đích
- **netDb/** (thư mục): Cơ sở dữ liệu đồng đẳng - thông tin router cho các nút tham gia mạng
- **peerProfiles/** (thư mục): Thống kê hiệu năng về các nút đồng đẳng - ảnh hưởng đến việc chọn tunnel
- **keyData/** (thư mục): Khóa đích cho eepsites và dịch vụ - mất sẽ làm thay đổi địa chỉ
- **addressbook/** (thư mục): Ánh xạ tên máy chủ .i2p cục bộ

**Quy trình sao lưu hoàn chỉnh** trước khi thực hiện các thay đổi:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Các dấu hiệu tập tin Router.config bị hỏng:**

- Router không khởi động với các lỗi phân tích cú pháp trong nhật ký
- Cài đặt không được giữ nguyên sau khi khởi động lại
- Xuất hiện các giá trị mặc định bất ngờ  
- Ký tự hiển thị bị lỗi khi xem tệp

**Sửa router.config bị hỏng:**

1. Sao lưu tệp hiện có: `cp router.config router.config.broken`
2. Kiểm tra mã hóa tệp: Phải là UTF-8 không có BOM
3. Xác minh cú pháp: Khóa dùng dấu phân tách `=` (không phải `:`), không có khoảng trắng ở cuối tên khóa, `#` chỉ dùng cho chú thích
4. Các lỗi hỏng phổ biến: Ký tự không phải ASCII trong giá trị, vấn đề ký tự kết thúc dòng (CRLF vs LF)
5. Nếu không thể sửa: Xóa router.config - router sẽ tạo cấu hình mặc định, giữ nguyên danh tính

**Các cài đặt router.config thiết yếu cần giữ nguyên:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**Mất hoặc tệp router.keys không hợp lệ** sẽ tạo ra một danh tính router mới. Điều này được chấp nhận, trừ khi:

- Vận hành floodfill (mất trạng thái floodfill)
- Lưu trữ eepsites với địa chỉ đã công khai (mất tính liên tục)  
- Danh tiếng đã được xây dựng trong mạng

Không thể khôi phục nếu không có bản sao lưu - hãy tạo mới: delete router.keys, restart I2P, danh tính mới sẽ được tạo.

**Phân biệt quan trọng:** router.keys (danh tính) so với keyData/* (dịch vụ). Mất router.keys sẽ làm thay đổi danh tính của router. Mất keyData/mysite-keys.dat sẽ làm thay đổi địa chỉ .i2p của eepsite (trang web trên I2P) của bạn - thảm họa nếu địa chỉ đã được công bố.

**Sao lưu riêng các khóa eepsite/dịch vụ:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Hỏng dữ liệu NetDb và peerProfiles:**

Triệu chứng: Không có peer (nút ngang hàng) nào đang hoạt động, không thể thiết lập tunnels, xuất hiện "Phát hiện hỏng cơ sở dữ liệu" trong nhật ký

Cách khắc phục an toàn (tất cả sẽ reseed (nạp lại seed ban đầu)/xây dựng lại tự động):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Các thư mục này chỉ chứa thông tin mạng được lưu đệm — xóa chúng sẽ buộc thực hiện bootstrap (khởi tạo ban đầu) mới, nhưng không làm mất dữ liệu quan trọng nào.

**Chiến lược phòng ngừa:**

1. **Luôn tắt đúng cách:** Dùng `i2prouter stop` hoặc nút "Shutdown" trên bảng điều khiển của router - không bao giờ kill cưỡng bức
2. **Sao lưu tự động:** Thiết lập tác vụ cron sao lưu hàng tuần ~/.i2p sang đĩa riêng biệt
3. **Giám sát tình trạng đĩa:** Kiểm tra trạng thái SMART định kỳ - đĩa lỗi làm hỏng dữ liệu
4. **Đủ dung lượng đĩa:** Duy trì từ 1 GB trống trở lên - đĩa đầy gây hỏng dữ liệu
5. **Khuyến nghị dùng UPS (bộ lưu điện):** Mất điện trong khi ghi sẽ làm hỏng tệp
6. **Kiểm soát phiên bản các cấu hình quan trọng:** Dùng kho Git cho router.config, i2ptunnel.config để có thể quay lui

**Quyền truy cập tệp rất quan trọng:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Giải mã các thông báo lỗi thường gặp

Ghi log của I2P cung cấp các thông báo lỗi cụ thể để chỉ ra chính xác vấn đề. Việc hiểu các thông báo này giúp đẩy nhanh quá trình khắc phục sự cố.

**"No tunnels available"** xuất hiện khi router chưa xây dựng đủ tunnel để hoạt động. Điều này là **bình thường trong 5-10 phút đầu tiên** sau khi khởi động. Nếu tình trạng này kéo dài quá 15 phút:

1. Xác minh Active Peers > 10 tại http://127.0.0.1:7657
2. Kiểm tra phân bổ băng thông có đủ (tối thiểu 128+ KB/giây)
3. Xem xét tỷ lệ thành công của tunnel tại http://127.0.0.1:7657/tunnels (nên >40%)
4. Xem lại nhật ký để tìm các lý do bị từ chối xây dựng tunnel

**"Clock skew detected"** hoặc **"NTCP2 disconnect code 7"** cho biết thời gian hệ thống lệch so với đồng thuận của mạng hơn 90 giây. I2P yêu cầu **độ chính xác ±60 giây**. Các kết nối với các router có thời gian lệch sẽ tự động bị từ chối.

Khắc phục ngay:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** hoặc **"Tunnel build timeout exceeded"** có nghĩa là việc xây dựng tunnel thông qua chuỗi peer (chuỗi nút ngang hàng) không hoàn tất trong cửa sổ thời gian chờ (thường là 60 giây). Nguyên nhân:

- **Các nút chậm:** Router đã chọn các nút tham gia không phản hồi cho tunnel
- **Tắc nghẽn mạng:** Mạng I2P đang chịu tải cao
- **Băng thông không đủ:** Giới hạn băng thông của bạn ngăn cản việc xây dựng tunnel kịp thời
- **Router quá tải:** Có quá nhiều tunnels tham gia đang tiêu tốn tài nguyên

Giải pháp: Tăng băng thông, giảm số lượng tunnels tham gia (`router.maxParticipatingTunnels` tại http://127.0.0.1:7657/configadvanced), bật chuyển tiếp cổng (port forwarding) để chọn nút ngang hàng tốt hơn.

**"Router is shutting down"** hoặc **"Graceful shutdown in progress"** xuất hiện trong quá trình tắt bình thường hoặc khi khôi phục sau sự cố. Việc tắt an toàn có thể mất **tối đa 10 phút** khi router đóng các tunnel, thông báo cho các nút ngang hàng và ghi lưu trạng thái.

Nếu bị kẹt trong trạng thái tắt quá 11 phút, hãy buộc kết thúc:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** báo hiệu tình trạng cạn kiệt heap (vùng nhớ cấp phát động). Giải pháp tức thời:

1. Chỉnh sửa wrapper.config: `wrapper.java.maxmemory=512` (hoặc cao hơn)
2. **Yêu cầu tắt hoàn toàn** - việc khởi động lại sẽ không áp dụng thay đổi
3. Chờ 11 phút để tắt hoàn toàn  
4. Khởi động router mới hoàn toàn
5. Xác minh phân bổ bộ nhớ tại http://127.0.0.1:7657/graphs - nên hiển thị headroom (khoảng trống)

**Các lỗi liên quan đến bộ nhớ:**

- **"GC overhead limit exceeded":** Tốn quá nhiều thời gian cho thu gom rác (garbage collection) - tăng dung lượng heap
- **"Metaspace":** Hết dung lượng không gian metadata của lớp Java - thêm `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Dành riêng cho Windows:** Kaspersky Antivirus giới hạn heap Java ở 512MB bất chấp các thiết lập trong wrapper.config - hãy gỡ cài đặt hoặc thêm I2P vào danh sách loại trừ.

**"Hết thời gian kết nối"** hoặc **"I2CP Error - port 7654"** khi các ứng dụng cố gắng kết nối tới router:

1. Xác minh router đang chạy: http://127.0.0.1:7657 nên phản hồi
2. Kiểm tra cổng I2CP: `netstat -an | grep 7654` nên hiển thị LISTENING
3. Đảm bảo tường lửa trên localhost cho phép: `sudo ufw allow from 127.0.0.1`  
4. Xác minh ứng dụng đang sử dụng đúng cổng (I2CP=7654, SAM=7656)

**"Certificate validation failed"** hoặc **"RouterInfo corrupt"** trong quá trình reseed (khởi tạo netDb ban đầu):

Nguyên nhân gốc: Lệch đồng hồ (khắc phục trước), netDb bị hỏng, chứng chỉ reseed (khởi tạo ban đầu) không hợp lệ

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Phát hiện hỏng cơ sở dữ liệu"** cho biết có hỏng dữ liệu ở mức đĩa trong netDb hoặc peerProfiles:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Kiểm tra sức khỏe ổ đĩa bằng các công cụ SMART (công nghệ tự giám sát, phân tích và báo cáo) - tình trạng hỏng dữ liệu tái diễn cho thấy bộ lưu trữ đang sắp hỏng.

## Thách thức đặc thù theo nền tảng

Các hệ điều hành khác nhau đặt ra những thách thức triển khai I2P mang tính đặc thù, liên quan đến quyền truy cập, chính sách bảo mật và tích hợp hệ thống.

### Các vấn đề về quyền và dịch vụ trên Linux

I2P được cài đặt từ gói chạy dưới tài khoản hệ thống **i2psvc** (Debian/Ubuntu) hoặc **i2p** (các bản phân phối khác), và cần các quyền cụ thể:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Giới hạn mô tả tệp (file descriptor)** ảnh hưởng đến khả năng xử lý kết nối của router. Giới hạn mặc định (1024) không đủ cho các router băng thông cao:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**Xung đột AppArmor** thường gặp trên Debian/Ubuntu ngăn chặn việc khởi động dịch vụ:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**Các vấn đề về SELinux** trên RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Khắc phục sự cố dịch vụ SystemD:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Sự can thiệp từ Tường lửa và phần mềm diệt virus trên Windows

Windows Defender và các sản phẩm chống virus của bên thứ ba thường xuyên đánh dấu I2P do các mẫu hành vi mạng. Cấu hình đúng cách giúp ngăn tình trạng chặn không cần thiết đồng thời vẫn duy trì bảo mật.

**Cấu hình Tường lửa Windows Defender:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Hãy thay cổng 22648 bằng cổng I2P thực tế của bạn từ http://127.0.0.1:7657/confignet.

**Sự cố cụ thể với Kaspersky Antivirus:** "Application Control" của Kaspersky giới hạn heap Java ở mức 512MB, bất kể các thiết lập trong wrapper.config. Điều này gây ra OutOfMemoryError (lỗi hết bộ nhớ) trên các routers băng thông cao.

Giải pháp: 1. Thêm I2P vào danh sách ngoại lệ của Kaspersky: Settings → Additional → Threats and Exclusions → Manage Exclusions 2. Hoặc gỡ cài đặt Kaspersky (được khuyến nghị cho việc vận hành I2P)

**Hướng dẫn chung về phần mềm diệt virus của bên thứ ba:**

- Thêm thư mục cài đặt I2P vào danh sách loại trừ  
- Thêm %APPDATA%\I2P và %LOCALAPPDATA%\I2P vào danh sách loại trừ
- Loại trừ javaw.exe khỏi phân tích hành vi
- Tắt các tính năng "Network Attack Protection" có thể can thiệp vào các giao thức I2P

### macOS Gatekeeper (tính năng bảo vệ của macOS) chặn cài đặt

macOS Gatekeeper (cơ chế kiểm soát bảo mật của macOS) ngăn các ứng dụng chưa được ký chạy. Các trình cài đặt I2P không được ký bằng Apple Developer ID (chứng danh nhà phát triển của Apple), gây ra cảnh báo bảo mật.

**Bỏ qua Gatekeeper (hệ thống bảo vệ ứng dụng của macOS) cho trình cài đặt I2P:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Việc chạy sau khi cài đặt** vẫn có thể kích hoạt cảnh báo:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Không bao giờ vô hiệu hóa Gatekeeper (cơ chế bảo vệ của macOS) vĩnh viễn** - gây rủi ro bảo mật cho các ứng dụng khác. Chỉ sử dụng cách bỏ qua theo từng tệp.

**Cấu hình tường lửa trên macOS:**

1. Tùy chọn hệ thống → Bảo mật & Quyền riêng tư → Tường lửa → Tùy chọn Tường lửa
2. Nhấp "+" để thêm ứng dụng  
3. Đi tới vị trí cài đặt Java (ví dụ, `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Thêm và đặt thành "Allow incoming connections"

### Các sự cố của ứng dụng I2P trên Android

Các ràng buộc về phiên bản Android và những hạn chế về tài nguyên tạo ra những thách thức riêng biệt.

**Yêu cầu tối thiểu:** - Yêu cầu Android 5.0+ (API level 21+) cho các phiên bản hiện tại - Tối thiểu 512MB RAM, khuyến nghị 1GB+   - 100MB dung lượng lưu trữ cho ứng dụng + dữ liệu router - Tắt hạn chế ứng dụng chạy nền cho I2P

**Ứng dụng bị sập ngay lập tức:**

1. **Kiểm tra phiên bản Android:** Cài đặt → Giới thiệu về điện thoại → Phiên bản Android (phải từ 5.0 trở lên)
2. **Gỡ cài đặt tất cả các phiên bản I2P:** Chỉ cài một biến thể:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Cài đặt nhiều phiên bản sẽ gây xung đột
3. **Xóa dữ liệu ứng dụng:** Cài đặt → Ứng dụng → I2P → Bộ nhớ → Xóa dữ liệu
4. **Cài đặt lại từ trạng thái sạch**

**Tối ưu hóa pin đang tắt router:**

Android mạnh tay đóng các ứng dụng chạy nền để tiết kiệm pin. I2P cần được đưa vào danh sách ngoại lệ:

1. Cài đặt → Pin → Tối ưu hóa pin (hoặc Sử dụng pin của ứng dụng)
2. Tìm I2P → Không tối ưu hóa (hoặc Cho phép hoạt động nền)
3. Cài đặt → Ứng dụng → I2P → Pin → Cho phép hoạt động nền + Gỡ bỏ hạn chế

**Sự cố kết nối trên di động:**

- **Khởi tạo cần WiFi:** Lần reseed (tải danh sách nút ban đầu) tải xuống một lượng dữ liệu đáng kể - hãy dùng WiFi, không dùng mạng di động
- **Thay đổi mạng:** I2P không xử lý việc chuyển mạng tốt - hãy khởi động lại ứng dụng sau khi chuyển giữa WiFi/mạng di động
- **Băng thông cho di động:** Cấu hình thận trọng ở mức 64-128 KB/giây để tránh hết dữ liệu di động

**Tối ưu hóa hiệu năng cho thiết bị di động:**

1. I2P app → Menu → Settings → Bandwidth
2. Đặt giới hạn phù hợp: 64 KB/sec vào, 32 KB/sec ra cho mạng di động
3. Giảm số lượng tunnels tham gia: Settings → Advanced → Max participating tunnels: 100-200
4. Bật "Stop I2P when screen off" để tiết kiệm pin

**Tải torrent trên Android:**

- Giới hạn tối đa 2-3 torrent chạy đồng thời
- Giảm mức độ tích cực của DHT  
- Chỉ dùng WiFi để torrent
- Chấp nhận tốc độ chậm hơn trên phần cứng di động

## Các vấn đề về Reseed (tải dữ liệu khởi tạo mạng) và bootstrap (khởi tạo ban đầu)

Cài đặt I2P mới cần **reseeding** (tải thông tin peer ban đầu) - lấy thông tin peer ban đầu từ các máy chủ HTTPS công khai để tham gia mạng. Sự cố reseed khiến người dùng bị kẹt trong tình trạng không có peer nào và không thể truy cập mạng.

**"No active peers" sau khi cài đặt mới** thường cho thấy việc reseed (tải dữ liệu khởi tạo) thất bại. Triệu chứng:

- Peer đã biết: 0 hoặc luôn dưới 5
- "Network: Testing" vẫn hiển thị sau hơn 15 phút
- Nhật ký cho thấy "Reseed failed" (reseed: tải danh sách peer khởi tạo) hoặc lỗi kết nối tới máy chủ reseed

**Vì sao reseed (tải dữ liệu khởi tạo mạng) thất bại:**

1. **Tường lửa chặn HTTPS:** Tường lửa của doanh nghiệp/ISP chặn kết nối tới reseed server (máy chủ khởi tạo mạng I2P) (port 443)
2. **Lỗi chứng chỉ SSL:** Hệ thống thiếu các chứng chỉ gốc được cập nhật
3. **Yêu cầu proxy:** Mạng yêu cầu proxy HTTP/SOCKS cho các kết nối ra ngoài
4. **Sai lệch đồng hồ:** Xác thực chứng chỉ SSL thất bại khi thời gian hệ thống sai
5. **Kiểm duyệt theo địa lý:** Một số quốc gia/ISP chặn các reseed server đã biết

**Buộc reseed (tải lại dữ liệu khởi tạo mạng) thủ công:**

1. Truy cập http://127.0.0.1:7657/configreseed
2. Nhấp "Save changes and reseed now"  
3. Theo dõi http://127.0.0.1:7657/logs để tìm "Reseed got XX router infos"
4. Chờ 5-10 phút để xử lý
5. Kiểm tra http://127.0.0.1:7657 - Known peers nên tăng lên 50+

**Cấu hình proxy reseed** cho các mạng bị hạn chế:

http://127.0.0.1:7657/configreseed → Cấu hình proxy:

- HTTP Proxy: [proxy-server]:[port]
- Hoặc SOCKS5: [socks-server]:[port]  
- Bật "Use proxy for reseed only"
- Thông tin đăng nhập (nếu cần)
- Lưu và buộc reseed (tải lại dữ liệu khởi tạo mạng)

**Lựa chọn thay thế: Proxy Tor cho reseed (khởi tạo netDb):**

Nếu Tor Browser hoặc Tor daemon (trình nền Tor) đang chạy:

- Loại proxy: SOCKS5
- Máy chủ: 127.0.0.1
- Cổng: 9050 (cổng SOCKS mặc định của Tor)
- Bật và reseed (tải lại dữ liệu khởi tạo mạng)

**Tái gieo (reseed) thủ công qua tệp su3** (biện pháp cuối cùng):

Khi tất cả các phương thức reseed (quy trình tải dữ liệu khởi tạo netDb) tự động đều thất bại, hãy lấy tệp reseed qua kênh out-of-band (ngoài băng):

1. Tải i2pseeds.su3 từ nguồn đáng tin cậy trên kết nối không bị hạn chế (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Dừng I2P hoàn toàn
3. Sao chép i2pseeds.su3 vào thư mục ~/.i2p/  
4. Khởi động I2P - tự động giải nén và xử lý tệp
5. Xóa i2pseeds.su3 sau khi xử lý
6. Xác minh số lượng nút tăng tại http://127.0.0.1:7657

**Lỗi chứng chỉ SSL trong quá trình reseed (khởi tạo dữ liệu mạng ban đầu):**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Giải pháp:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Bị kẹt ở 0 nút ngang hàng đã biết quá 30 phút:**

Cho biết việc reseed (khởi tạo netDb ban đầu từ các máy chủ reseed) đã thất bại hoàn toàn. Trình tự khắc phục sự cố:

1. **Xác minh thời gian hệ thống là chính xác** (sự cố phổ biến nhất - sửa TRƯỚC)
2. **Kiểm tra kết nối HTTPS:** Thử truy cập https://reseed.i2p.rocks trong trình duyệt - nếu thất bại, là sự cố mạng
3. **Kiểm tra nhật ký I2P** tại http://127.0.0.1:7657/logs để tìm các lỗi reseed (nạp danh sách nút ban đầu) cụ thể
4. **Thử URL reseed khác:** http://127.0.0.1:7657/configreseed → thêm URL reseed tùy chỉnh: https://reseed-fr.i2pd.xyz/
5. **Sử dụng phương pháp tệp su3 thủ công** nếu đã thử hết các cách tự động

**Máy chủ reseed đôi khi ngoại tuyến:** I2P bao gồm nhiều máy chủ reseed được hardcoded (ghi cứng trong mã). Nếu một máy chủ gặp lỗi, router sẽ tự động thử các máy chủ khác. Trường hợp tất cả các máy chủ reseed đều thất bại hoàn toàn là cực kỳ hiếm nhưng vẫn có thể xảy ra.

**Các reseed servers (máy chủ cung cấp dữ liệu ban đầu cho netDb) hiện đang hoạt động** (tính đến tháng 10 năm 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Thêm dưới dạng URL tùy chỉnh nếu gặp sự cố với các thiết lập mặc định.

**Dành cho người dùng ở các khu vực bị kiểm duyệt gắt gao:**

Cân nhắc sử dụng các cầu Snowflake/Meek qua Tor cho reseed (tải dữ liệu khởi tạo mạng I2P) ban đầu, rồi chuyển sang I2P trực tiếp khi đã hòa mạng xong. Hoặc nhận i2pseeds.su3 qua steganography (giấu tin), email hoặc USB từ bên ngoài vùng kiểm duyệt.

## Khi nào nên tìm kiếm thêm sự trợ giúp

Hướng dẫn này bao quát đại đa số các vấn đề về I2P, nhưng một số vấn đề cần sự chú ý của nhà phát triển hoặc chuyên môn của cộng đồng.

**Nhờ cộng đồng I2P hỗ trợ khi:**

- Router liên tục bị sập sau khi đã thực hiện tất cả các bước khắc phục sự cố
- Rò rỉ bộ nhớ khiến mức sử dụng tăng đều, vượt quá heap (vùng nhớ heap) đã cấp phát
- Tỷ lệ thành công của Tunnel vẫn dưới 20% mặc dù đã cấu hình phù hợp  
- Các lỗi mới trong nhật ký không được đề cập trong hướng dẫn này
- Lỗ hổng bảo mật được phát hiện
- Yêu cầu tính năng hoặc đề xuất cải tiến

**Trước khi yêu cầu trợ giúp, hãy thu thập thông tin chẩn đoán:**

1. Phiên bản I2P: http://127.0.0.1:7657 (ví dụ: "2.10.0")
2. Phiên bản Java: đầu ra của `java -version`
3. Hệ điều hành và phiên bản
4. Tình trạng router: Trạng thái mạng, Số lượng peer (nút ngang hàng) đang hoạt động, Các tunnel tham gia
5. Cấu hình băng thông: Giới hạn vào/ra
6. Trạng thái chuyển tiếp cổng (port forwarding): Bị tường lửa chặn hoặc OK
7. Trích đoạn nhật ký liên quan: 50 dòng cuối hiển thị lỗi từ http://127.0.0.1:7657/logs

**Các kênh hỗ trợ chính thức:**

- **Diễn đàn:** https://i2pforum.net (clearnet — Internet thông thường) hoặc http://i2pforum.i2p (bên trong I2P)
- **IRC:** #i2p trên Irc2P (irc.postman.i2p qua I2P) hoặc irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p dành cho thảo luận của cộng đồng
- **Trình theo dõi lỗi:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues dành cho các lỗi đã được xác nhận
- **Danh sách thư:** i2p-dev@lists.i2p-projekt.de dành cho các câu hỏi về phát triển

**Kỳ vọng thực tế rất quan trọng.** I2P chậm hơn clearnet (mạng Internet công khai) do thiết kế nền tảng - tunneling được mã hóa đa hop tạo ra độ trễ vốn có. Một I2P router có thời gian tải trang 30 giây và tốc độ torrent 50 KB/sec là **đang hoạt động đúng**, không bị hỏng. Người dùng kỳ vọng tốc độ clearnet sẽ thất vọng, bất kể tối ưu cấu hình.

## Kết luận

Phần lớn các vấn đề I2P xuất phát từ ba nhóm: thiếu kiên nhẫn trong giai đoạn bootstrap (khởi động ban đầu) (cần 10–15 phút), phân bổ tài nguyên không đủ (tối thiểu 512 MB RAM, 256 KB/giây băng thông), hoặc cấu hình chuyển tiếp cổng sai. Việc hiểu kiến trúc phân tán và thiết kế tập trung vào tính ẩn danh của I2P giúp người dùng phân biệt hành vi mong đợi với các vấn đề thực sự.

Trạng thái "Firewalled" của router, tuy không tối ưu, không ngăn cản việc sử dụng I2P - chỉ hạn chế mức độ đóng góp cho mạng và làm giảm nhẹ hiệu năng. Người dùng mới nên ưu tiên **tính ổn định hơn tối ưu hóa**: hãy chạy router liên tục trong vài ngày trước khi điều chỉnh các cài đặt nâng cao, vì mức độ hòa nhập với mạng sẽ tự nhiên cải thiện theo thời gian hoạt động.

Khi khắc phục sự cố, hãy luôn kiểm tra các yếu tố cơ bản trước: thời gian hệ thống chính xác, băng thông đầy đủ, router chạy liên tục và tối thiểu 10 nút ngang hàng đang hoạt động. Phần lớn sự cố được giải quyết bằng cách xử lý những điều cơ bản này thay vì chỉnh các tham số cấu hình khó hiểu. I2P sẽ đền đáp sự kiên nhẫn và việc vận hành liên tục bằng hiệu năng được cải thiện, khi router xây dựng uy tín và tối ưu hóa việc chọn nút ngang hàng qua nhiều ngày và nhiều tuần hoạt động.
