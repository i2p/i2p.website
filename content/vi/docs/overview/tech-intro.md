---
title: "I2P: Một framework có khả năng mở rộng cho truyền thông ẩn danh"
description: "Giới thiệu kỹ thuật về kiến trúc và hoạt động của I2P"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Giới thiệu

I2P là một lớp mạng ẩn danh chuyển mạch gói có khả năng mở rộng, tự tổ chức và bền vững, trên đó có thể vận hành nhiều ứng dụng khác nhau quan tâm đến tính ẩn danh hoặc bảo mật. Mỗi ứng dụng này có thể đưa ra sự đánh đổi riêng giữa tính ẩn danh, độ trễ và thông lượng mà không cần lo lắng về việc triển khai đúng đắn của một free route mixnet, cho phép chúng hòa trộn hoạt động của mình với tập hợp lớn hơn các người dùng ẩn danh đã đang chạy trên I2P.

Các ứng dụng hiện có cung cấp đầy đủ các hoạt động Internet thông thường — duyệt web **ẩn danh**, lưu trữ web, trò chuyện, chia sẻ tệp, email, blog và phân phối nội dung, cùng với một số ứng dụng khác đang được phát triển.

- **Duyệt web:** sử dụng bất kỳ trình duyệt nào hỗ trợ proxy  
- **Trò chuyện:** IRC và các giao thức khác  
- **Chia sẻ tệp:** [I2PSnark](#i2psnark) và các ứng dụng khác  
- **E-mail:** [Susimail](#i2pmail) và các ứng dụng khác  
- **Blog:** sử dụng bất kỳ máy chủ web cục bộ nào, hoặc các plugin có sẵn

Không giống như các trang web được lưu trữ trong các mạng phân phối nội dung như [Freenet](/docs/overview/comparison#freenet) hay [GNUnet](https://www.gnunet.org/), các dịch vụ được lưu trữ trên I2P có khả năng tương tác đầy đủ — có các công cụ tìm kiếm theo phong cách web truyền thống, diễn đàn, blog mà bạn có thể bình luận, các trang web dựa trên cơ sở dữ liệu, và các cầu nối để truy vấn các hệ thống tĩnh như Freenet mà không cần cài đặt chúng trên máy cục bộ.

Với tất cả các ứng dụng hỗ trợ ẩn danh này, I2P hoạt động như **middleware hướng thông điệp** — các ứng dụng chỉ định dữ liệu cần gửi đến một định danh mật mã (một "destination"), và I2P đảm bảo nó đến nơi một cách an toàn và ẩn danh. I2P cũng bao gồm một [thư viện streaming](#streaming) đơn giản để cho phép các thông điệp best-effort ẩn danh của I2P truyền tải như các luồng đáng tin cậy, theo thứ tự, cung cấp kiểm soát tắc nghẽn dựa trên TCP được điều chỉnh cho tích số băng thông-độ trễ cao của mạng.

Mặc dù các SOCKS proxy đơn giản đã được phát triển để kết nối các ứng dụng hiện có, giá trị của chúng bị hạn chế vì hầu hết các ứng dụng đều làm rò rỉ thông tin nhạy cảm trong ngữ cảnh ẩn danh. Cách tiếp cận an toàn nhất là **kiểm toán và điều chỉnh** ứng dụng để sử dụng trực tiếp các API của I2P.

I2P không phải là một dự án nghiên cứu — học thuật, thương mại hay chính phủ — mà là một nỗ lực kỹ thuật nhằm cung cấp tính ẩn danh có thể sử dụng được. Dự án đã được phát triển liên tục từ đầu năm 2003 bởi một nhóm cộng tác viên phân tán trên toàn thế giới. Tất cả các công trình I2P đều là **mã nguồn mở** trên [trang web chính thức](https://geti2p.net/), chủ yếu được phát hành vào phạm vi công cộng, với một số thành phần sử dụng giấy phép BSD-style linh hoạt. Một số ứng dụng khách có giấy phép GPL cũng có sẵn, chẳng hạn như [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail), và [I2PSnark](#i2psnark). Nguồn tài trợ hoàn toàn đến từ các khoản đóng góp của người dùng.

---

## Vận hành

### Overview

I2P phân biệt rõ ràng giữa router (các nút tham gia vào mạng lưới) và destination (các điểm cuối ẩn danh cho ứng dụng). Việc chạy I2P tự nó không phải là bí mật; điều được ẩn giấu là **những gì** người dùng đang làm và router nào mà các destination của họ sử dụng. Người dùng cuối thường chạy nhiều destination (ví dụ: một cho duyệt web, một cho hosting, một cho IRC).

Một khái niệm quan trọng trong I2P là **tunnel** — một đường dẫn mã hóa một chiều đi qua một chuỗi các router. Mỗi router chỉ giải mã một lớp và chỉ biết điểm chuyển tiếp tiếp theo. Các tunnel hết hạn sau mỗi 10 phút và phải được xây dựng lại.

![Sơ đồ tunnel đến và tunnel đi](/images/tunnels.png)   *Hình 1: Tồn tại hai loại tunnel — inbound (đến) và outbound (đi).*

- **Tunnel gửi đi (Outbound tunnels)** gửi tin nhắn ra khỏi người tạo.  
- **Tunnel nhận về (Inbound tunnels)** mang tin nhắn trở lại cho người tạo.

Kết hợp các tunnel này cho phép giao tiếp hai chiều. Ví dụ, "Alice" sử dụng một outbound tunnel để gửi tới inbound tunnel của "Bob". Alice mã hóa tin nhắn của mình kèm theo hướng dẫn định tuyến tới inbound gateway của Bob.

Một khái niệm quan trọng khác là **network database** hoặc **netDb**, cơ sở dữ liệu phân tán các siêu dữ liệu về router và điểm đến:

- **RouterInfo:** Chứa thông tin liên lạc và khóa mật mã của router.  
- **LeaseSet:** Chứa thông tin cần thiết để liên lạc với một đích đến (các cổng tunnel, thời gian hết hạn, khóa mã hóa).

Các router công bố RouterInfo của chúng trực tiếp lên netDb; các LeaseSet được gửi qua các tunnel đi ra để đảm bảo tính ẩn danh.

Để xây dựng tunnel, Alice truy vấn netDb để lấy các mục RouterInfo nhằm chọn peer, và gửi các thông điệp xây dựng tunnel được mã hóa qua từng hop cho đến khi tunnel hoàn thành.

![Thông tin router được sử dụng để xây dựng các tunnel](/images/netdb_get_routerinfo_2.png)   *Hình 2: Thông tin router được sử dụng để xây dựng các tunnel.*

Để gửi dữ liệu đến Bob, Alice tra cứu LeaseSet của Bob và sử dụng một trong các tunnel đi của mình để định tuyến dữ liệu qua cổng vào của tunnel đến của Bob.

![LeaseSets kết nối các tunnel đến và đi](/images/netdb_get_leaseset.png)   *Hình 3: LeaseSets kết nối các tunnel đi và tunnel đến.*

Bởi vì I2P dựa trên thông điệp, nó bổ sung **mã hóa garlic đầu-cuối** để bảo vệ thông điệp ngay cả khỏi điểm cuối đi ra hoặc cổng vào. Một thông điệp garlic bao gồm nhiều "clove" (thông điệp) được mã hóa để che giấu metadata và cải thiện tính ẩn danh.

Các ứng dụng có thể sử dụng trực tiếp giao diện tin nhắn hoặc dựa vào [thư viện streaming](#streaming) để có kết nối đáng tin cậy.

---

### Tunnels

Cả tunnel đến và tunnel đi đều sử dụng mã hóa nhiều lớp, nhưng khác nhau về cấu trúc:

- Trong **inbound tunnels**, người tạo (endpoint) giải mã tất cả các lớp.
- Trong **outbound tunnels**, người tạo (gateway) giải mã trước các lớp để đảm bảo rõ ràng tại endpoint.

I2P phân tích hồ sơ của các peer thông qua các chỉ số gián tiếp như độ trễ và độ tin cậy mà không cần thăm dò trực tiếp. Dựa trên các hồ sơ này, các peer được nhóm động vào bốn cấp độ:

1. Nhanh và dung lượng cao  
2. Dung lượng cao  
3. Không lỗi  
4. Đang lỗi

Việc lựa chọn peer cho tunnel thường ưu tiên các peer có băng thông cao, được chọn ngẫu nhiên để cân bằng giữa tính ẩn danh và hiệu suất, với các chiến lược sắp xếp bổ sung dựa trên XOR để giảm thiểu các cuộc tấn công predecessor và thu thập netDb.

Để biết thêm chi tiết, xem [Thông số kỹ thuật Tunnel](/docs/specs/implementation).

---

### Tổng quan

Các router tham gia vào bảng băm phân tán (DHT) **floodfill** lưu trữ và phản hồi các truy vấn LeaseSet. DHT sử dụng một biến thể của [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Các router floodfill được chọn tự động nếu chúng có đủ năng lực và tính ổn định, hoặc có thể được cấu hình thủ công.

- **RouterInfo:** Mô tả khả năng và các phương thức truyền tải của router.  
- **LeaseSet:** Mô tả các tunnel và khóa mã hóa của đích đến.

Tất cả dữ liệu trong netDb đều được ký bởi người xuất bản và đánh dấu thời gian để ngăn chặn các cuộc tấn công phát lại hoặc sử dụng mục tin cũ. Đồng bộ hóa thời gian được duy trì thông qua SNTP và phát hiện độ lệch tại tầng vận chuyển.

#### Additional concepts

- **LeaseSet không công khai và được mã hóa:**  
  Một destination có thể duy trì tính riêng tư bằng cách không công khai LeaseSet của mình, chỉ chia sẻ với các peer đáng tin cậy. Việc truy cập yêu cầu khóa giải mã phù hợp.

- **Bootstrapping (reseeding):**  
  Để tham gia mạng lưới, một router mới tải các tệp RouterInfo đã ký từ các máy chủ reseed HTTPS đáng tin cậy.

- **Khả năng mở rộng tra cứu:**  
  I2P sử dụng tra cứu **lặp (iterative)**, không phải đệ quy (recursive), để cải thiện khả năng mở rộng và bảo mật của DHT.

---

### Tunnels

Giao tiếp I2P hiện đại sử dụng hai phương thức truyền tải được mã hóa hoàn toàn:

- **[NTCP2](/docs/specs/ntcp2):** Giao thức mã hóa dựa trên TCP  
- **[SSU2](/docs/specs/ssu2):** Giao thức mã hóa dựa trên UDP

Cả hai đều được xây dựng trên [Noise Protocol Framework](https://noiseprotocol.org/) hiện đại, cung cấp xác thực mạnh mẽ và khả năng chống nhận dạng lưu lượng. Chúng đã thay thế các giao thức NTCP và SSU cũ (đã ngừng hoàn toàn từ năm 2023).

**NTCP2** cung cấp truyền tải dữ liệu được mã hóa, hiệu quả qua TCP.

**SSU2** cung cấp độ tin cậy dựa trên UDP, khả năng vượt qua NAT và tùy chọn xuyên thủng lỗ (hole punching). SSU2 về mặt khái niệm tương tự như WireGuard hoặc QUIC, cân bằng giữa độ tin cậy và tính ẩn danh.

Router có thể hỗ trợ cả IPv4 và IPv6, công bố địa chỉ vận chuyển và chi phí của chúng trong netDb. Phương thức vận chuyển của một kết nối được chọn động thông qua **hệ thống đấu thầu** tối ưu hóa cho các điều kiện và liên kết hiện có.

---

### Cơ sở dữ liệu mạng (netDb)

I2P sử dụng mật mã phân lớp cho tất cả các thành phần: giao vận, tunnel, garlic messages và network database.

Các nguyên hàm hiện tại bao gồm:

- X25519 cho trao đổi khóa  
- EdDSA (Ed25519) cho chữ ký số  
- ChaCha20-Poly1305 cho mã hóa xác thực  
- SHA-256 cho băm  
- AES256 cho mã hóa lớp tunnel

Các thuật toán cũ (ElGamal, DSA-SHA1, ECDSA) vẫn được giữ lại để tương thích ngược.

I2P hiện đang giới thiệu các sơ đồ mật mã lai hậu lượng tử (PQ) kết hợp **X25519** với **ML-KEM** để chống lại các cuộc tấn công "thu thập ngay, giải mã sau".

#### Garlic Messages

Garlic messages mở rộng onion routing bằng cách nhóm nhiều "cloves" được mã hóa với các chỉ dẫn gửi độc lập. Điều này cho phép tính linh hoạt trong định tuyến ở cấp độ thông điệp và đồng nhất hóa lưu lượng.

#### Session Tags

Hai hệ thống mã hóa được hỗ trợ cho mã hóa đầu-cuối:

- **ElGamal/AES+SessionTags (cũ):**  
  Sử dụng session tags được gửi trước như nonce 32-byte. Hiện đã không được khuyến nghị do kém hiệu quả.

- **ECIES-X25519-AEAD-Ratchet (hiện tại):**  
  Sử dụng ChaCha20-Poly1305 và PRNG dựa trên HKDF được đồng bộ hóa để tạo các khóa phiên tạm thời và thẻ 8-byte một cách động, giảm thiểu chi phí CPU, bộ nhớ và băng thông trong khi vẫn duy trì tính bảo mật chuyển tiếp.

---

## Future of the Protocol

Các lĩnh vực nghiên cứu chính tập trung vào việc duy trì bảo mật chống lại các đối thủ cấp quốc gia và giới thiệu các biện pháp bảo vệ hậu lượng tử. Hai khái niệm thiết kế ban đầu — **restricted routes** và **variable latency** — đã được thay thế bởi các phát triển hiện đại.

### Restricted Route Operation

Các khái niệm định tuyến hạn chế ban đầu nhằm mục đích che giấu địa chỉ IP. Nhu cầu này đã phần lớn được giảm thiểu bởi:

- UPnP cho chuyển tiếp cổng tự động
- Vượt qua NAT mạnh mẽ trong SSU2
- Hỗ trợ IPv6
- Introducers (người giới thiệu) hợp tác và NAT hole-punching (kỹ thuật xuyên thủng NAT)
- Kết nối overlay (lớp phủ) tùy chọn (ví dụ: Yggdrasil)

Do đó, I2P hiện đại đạt được các mục tiêu tương tự một cách thực tế hơn mà không cần định tuyến hạn chế phức tạp.

---

## Similar Systems

I2P tích hợp các khái niệm từ middleware hướng thông điệp (message-oriented middleware), DHT (bảng băm phân tán), và mixnet (mạng trộn lẫn). Sự đổi mới của nó nằm ở việc kết hợp những thành phần này thành một nền tảng ẩn danh tự tổ chức và có thể sử dụng được.

### Các Giao Thức Truyền Tải

*[Trang web](https://www.torproject.org/)*

**Tor** và **I2P** có chung mục tiêu nhưng khác nhau về kiến trúc:

- **Tor:** Chuyển mạch theo mạch; phụ thuộc vào các directory authorities đáng tin cậy. (~10k relay)  
- **I2P:** Chuyển mạch theo gói; mạng lưới phân tán hoàn toàn dựa trên DHT. (~50k router)

Các tunnel đơn hướng của I2P để lộ ít metadata hơn và cho phép các đường định tuyến linh hoạt, trong khi Tor tập trung vào truy cập **Internet ẩn danh (outproxying - định tuyến ra ngoài)**.   Ngược lại, I2P hỗ trợ **lưu trữ ẩn danh trong mạng**.

### Mật mã học

*[Trang web](https://freenetproject.org/)*

**Freenet** tập trung vào việc công bố và truy xuất tệp tin ẩn danh, lâu dài. **I2P**, ngược lại, cung cấp một **lớp truyền thông thời gian thực** cho việc sử dụng tương tác (web, chat, torrents). Kết hợp với nhau, hai hệ thống này bổ sung cho nhau — Freenet cung cấp khả năng lưu trữ chống kiểm duyệt; I2P cung cấp tính ẩn danh trong vận chuyển.

### Other Networks

- **Lokinet:** Mạng phủ dựa trên IP sử dụng các node dịch vụ được khuyến khích.  
- **Nym:** Mixnet thế hệ tiếp theo nhấn mạnh bảo vệ siêu dữ liệu với lưu lượng che giấu ở độ trễ cao hơn.

---

## Appendix A: Application Layer

Bản thân I2P chỉ xử lý việc truyền tải thông điệp. Chức năng tầng ứng dụng được triển khai bên ngoài thông qua các API và thư viện.

### Streaming Library {#streaming}

**Thư viện streaming** hoạt động như bản tương tự TCP của I2P, với giao thức cửa sổ trượt và kiểm soát tắc nghẽn được tinh chỉnh cho truyền tải ẩn danh có độ trễ cao.

Các mẫu yêu cầu/phản hồi HTTP điển hình thường có thể hoàn thành trong một lượt truyền dữ liệu duy nhất nhờ vào tối ưu hóa gộp thông điệp.

### Naming Library and Address Book

*Phát triển bởi: mihi, Ragnarok*   Xem trang [Danh pháp và Sổ địa chỉ](/docs/overview/naming).

Hệ thống đặt tên của I2P là **cục bộ và phi tập trung**, tránh việc sử dụng tên toàn cục theo kiểu DNS. Mỗi router duy trì một bảng ánh xạ cục bộ từ các tên dễ đọc sang các địa chỉ đích (destination). Các sổ địa chỉ tùy chọn dựa trên mạng lưới tin cậy có thể được chia sẻ hoặc nhập từ các nút đồng cấp đáng tin cậy.

Cách tiếp cận này tránh được các cơ quan tập trung và vượt qua các lỗ hổng Sybil vốn có trong các hệ thống đặt tên toàn cầu hoặc theo kiểu bỏ phiếu.

### Hoạt động Tuyến đường Hạn chế

*Phát triển bởi: mihi*

**I2PTunnel** là giao diện lớp client chính cho phép proxy TCP ẩn danh. Nó hỗ trợ:

- **Client tunnels** (đường hầm ra ngoài đến các điểm đích I2P)  
- **HTTP client (eepproxy)** cho tên miền ".i2p"  
- **Server tunnels** (đường hầm vào từ I2P đến dịch vụ cục bộ)  
- **HTTP server tunnels** (proxy an toàn cho các dịch vụ web)

Outproxying (ra Internet thông thường) là tùy chọn, được thực hiện bởi các tunnel "máy chủ" do tình nguyện viên vận hành.

### I2PSnark {#i2psnark}

*Phát triển bởi: jrandom, et al — chuyển đổi từ [Snark](http://www.klomp.org/snark/)*

Được tích hợp sẵn với I2P, **I2PSnark** là một BitTorrent client đa torrent ẩn danh với hỗ trợ DHT và UDP, có thể truy cập qua giao diện web.

### Tor

*Phát triển bởi: postman, susi23, mastiejaner*

**I2Pmail** cung cấp email ẩn danh thông qua các kết nối I2PTunnel. **Susimail** là một ứng dụng email dựa trên web được xây dựng đặc biệt để ngăn chặn rò rỉ thông tin thường gặp trong các ứng dụng email truyền thống. Dịch vụ [mail.i2p](https://mail.i2p/) có tính năng lọc virus, hạn ngạch [hashcash](https://en.wikipedia.org/wiki/Hashcash), và tách biệt outproxy để bảo vệ bổ sung.

---
