---
title: "SAM V3"
description: "Giao thức Gửi tin nhắn Ẩn danh Đơn giản dành cho các ứng dụng I2P không dùng Java"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM là một giao thức khách hàng đơn giản để tương tác với I2P. SAM là giao thức được khuyến nghị cho các ứng dụng không dùng Java khi kết nối với mạng I2P, và được hỗ trợ bởi nhiều triển khai router khác nhau. Các ứng dụng Java nên sử dụng trực tiếp các API streaming hoặc I2CP.

SAM phiên bản 3 được giới thiệu trong bản phát hành I2P 0.7.3 (tháng 5 năm 2009) và là một giao diện ổn định, được hỗ trợ. Phiên bản 3.1 cũng ổn định và hỗ trợ tùy chọn loại chữ ký, điều này được khuyến nghị mạnh mẽ. Các phiên bản 3.x gần đây hơn hỗ trợ các tính năng nâng cao. Lưu ý rằng i2pd hiện tại không hỗ trợ hầu hết các tính năng của 3.2 và 3.3.

Các lựa chọn thay thế: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (đã ngừng hỗ trợ)](/docs/api/bob). Các phiên bản đã ngừng hỗ trợ: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Các thư viện SAM đã biết

Cảnh báo: Một số liên kết có thể rất cũ hoặc không còn được hỗ trợ. Không có liên kết nào được dự án I2P kiểm tra, đánh giá hoặc duy trì, trừ khi được ghi chú bên dưới. Hãy tự nghiên cứu kỹ trước khi sử dụng.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Hướng dẫn nhanh

Để triển khai một ứng dụng ngang hàng cơ bản chỉ sử dụng TCP, máy khách phải hỗ trợ các lệnh sau:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Cần thiết cho tất cả các lệnh còn lại
- `DEST GENERATE SIGNATURE_TYPE=7` - Để tạo khóa riêng tư và đích đến (destination) của chúng ta
- `NAMING LOOKUP NAME=...` - Để chuyển đổi địa chỉ .i2p thành các đích đến
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Cần thiết cho lệnh STREAM CONNECT và STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - Để thực hiện kết nối đi ra ngoài
- `STREAM ACCEPT ID=...` - Để chấp nhận các kết nối vào

## Hướng dẫn chung cho các nhà phát triển

### Thiết kế Ứng dụng

Các phiên SAM (hoặc bên trong I2P, các nhóm đường hầm hay tập hợp các đường hầm) được thiết kế để tồn tại lâu dài. Hầu hết các ứng dụng chỉ cần một phiên, được tạo khi khởi động và đóng khi thoát. I2P khác với Tor, nơi các mạch có thể được tạo và loại bỏ nhanh chóng. Hãy cân nhắc kỹ và tham khảo ý kiến các nhà phát triển I2P trước khi thiết kế ứng dụng của bạn để sử dụng nhiều hơn một hoặc hai phiên đồng thời, hoặc để tạo và loại bỏ phiên một cách nhanh chóng. Hầu hết các mô hình đe dọa sẽ không yêu cầu một phiên riêng biệt cho mỗi kết nối.

Ngoài ra, vui lòng đảm bảo cài đặt ứng dụng của bạn (và hướng dẫn người dùng về cài đặt router, hoặc cài đặt mặc định của router nếu bạn tích hợp router) sẽ khiến người dùng đóng góp nhiều tài nguyên hơn vào mạng so với mức họ tiêu thụ. I2P là một mạng ngang hàng (peer-to-peer), và mạng sẽ không thể tồn tại nếu một ứng dụng phổ biến khiến mạng rơi vào tình trạng tắc nghẽn kéo dài.

### Tương thích và Kiểm thử

Các triển khai bộ định tuyến Java I2P và i2pd là độc lập và có một số khác biệt nhỏ về hành vi, hỗ trợ tính năng và thiết lập mặc định. Vui lòng kiểm thử ứng dụng của bạn với phiên bản mới nhất của cả hai bộ định tuyến.

i2pd SAM được bật theo mặc định; còn SAM của Java I2P thì không. Hãy cung cấp hướng dẫn cho người dùng về cách bật SAM trong Java I2P (thông qua /configclients trong bảng điều khiển router), và/hoặc hiển thị thông báo lỗi rõ ràng nếu việc kết nối ban đầu thất bại, ví dụ: "hãy đảm bảo rằng I2P đang chạy và giao diện SAM đã được bật".

Các bộ định tuyến Java I2P và i2pd có giá trị mặc định khác nhau về số lượng tunnel. Giá trị mặc định của Java là 2 và giá trị mặc định của i2pd là 5. Đối với hầu hết các trường hợp có băng thông thấp đến trung bình và số lượng kết nối thấp đến trung bình, con số 2 hoặc 3 là đủ. Vui lòng chỉ định số lượng tunnel trong tin nhắn SESSION CREATE để đạt được hiệu suất nhất quán khi sử dụng bộ định tuyến Java I2P và i2pd. Xem bên dưới.

Để biết thêm hướng dẫn dành cho các nhà phát triển nhằm đảm bảo ứng dụng của bạn chỉ sử dụng những tài nguyên cần thiết, vui lòng xem [hướng dẫn nhúng I2P vào ứng dụng của bạn](/docs/applications/embedding).

### Các loại chữ ký và mã hóa

I2P hỗ trợ nhiều loại chữ ký và mã hóa. Để đảm bảo tương thích ngược, SAM mặc định sử dụng các loại cũ và kém hiệu quả, do đó tất cả các client nên chỉ định các loại mới hơn.

Loại chữ ký được xác định trong các lệnh DEST GENERATE và SESSION CREATE (đối với phiên tạm thời). Tất cả các client nên đặt `SIGNATURE_TYPE=7` (Ed25519).

Loại mã hóa được chỉ định trong lệnh SESSION CREATE. Cho phép nhiều loại mã hóa. Người dùng nên đặt `i2cp.leaseSetEncType=4` (chỉ dùng ECIES-X25519) hoặc `i2cp.leaseSetEncType=6,4` (dùng MLKEM-768 và ECIES-X25519, dành cho các bộ định tuyến hỗ trợ API 0.9.67 trở lên).

## Thay đổi phiên bản 3

### Những thay đổi ở phiên bản 3.0

Phiên bản 3.0 được giới thiệu trong bản phát hành I2P 0.7.3. SAM v2 cung cấp cách quản lý nhiều socket trên cùng một điểm đến I2P *song song*, nghĩa là client không phải chờ dữ liệu được gửi thành công qua một socket trước khi gửi dữ liệu qua socket khác. Tuy nhiên, mọi dữ liệu đều đi qua cùng một socket từ client đến SAM, điều này khá phức tạp để quản lý đối với client.

SAM v3 quản lý các socket theo một cách khác: mỗi *socket I2P* tương ứng với một socket duy nhất từ client tới SAM, điều này đơn giản hơn nhiều trong việc xử lý. Cách này tương tự như [BOB](/docs/api/bob).

SAM v3 cũng cung cấp một cổng UDP để gửi các gói tin qua I2P, và có thể chuyển tiếp các gói tin I2P về máy chủ datagram của client.

### Thay đổi ở phiên bản 3.1

Phiên bản 3.1 được giới thiệu trong bản phát hành Java I2P 0.9.14 (tháng 7 năm 2014). SAM 3.1 là phiên bản triển khai SAM tối thiểu được khuyến nghị do hỗ trợ các loại chữ ký tốt hơn so với SAM 3.0. i2pd cũng hỗ trợ hầu hết các tính năng của phiên bản 3.1.

- DEST GENERATE và SESSION CREATE hiện đã hỗ trợ tham số SIGNATURE_TYPE.
- Các tham số MIN và MAX trong HELLO VERSION hiện là tùy chọn.
- Các tham số MIN và MAX trong HELLO VERSION hiện hỗ trợ các phiên bản một chữ số như "3".
- RAW SEND hiện đã được hỗ trợ trên cổng kết nối bridge.

### Thay đổi phiên bản 3.2

Phiên bản 3.2 được giới thiệu trong bản phát hành Java I2P 0.9.24 (tháng 1 năm 2016). Lưu ý rằng i2pd hiện tại không hỗ trợ hầu hết các tính năng 3.2.

#### Hỗ trợ cổng và giao thức I2CP

- Các tùy chọn FROM_PORT và TO_PORT trong SESSION CREATE
- Tùy chọn PROTOCOL trong SESSION CREATE với STYLE=RAW
- Các tùy chọn FROM_PORT và TO_PORT trong STREAM CONNECT, DATAGRAM SEND và RAW SEND
- Tùy chọn PROTOCOL trong RAW SEND
- DATAGRAM RECEIVED, RAW RECEIVED và các luồng hoặc datagram có thể trả lời được chuyển tiếp hoặc nhận về, bao gồm FROM_PORT và TO_PORT
- Tùy chọn phiên RAW HEADER=true sẽ khiến các datagram raw được chuyển tiếp được thêm vào đầu một dòng chứa PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- Dòng đầu tiên của các datagram gửi qua cổng 7655 giờ đây có thể bắt đầu bằng bất kỳ phiên bản 3.x nào
- Dòng đầu tiên của các datagram gửi qua cổng 7655 có thể chứa bất kỳ tùy chọn nào trong số FROM_PORT, TO_PORT, PROTOCOL
- RAW RECEIVED bao gồm PROTOCOL=nnn

#### SSL và Xác thực

- USER/PASSWORD trong các tham số HELLO để xác thực. Xem [phần dưới](#authorization).
- Cấu hình xác thực tùy chọn với lệnh AUTH. Xem [phần dưới](#authorization-configuration-sam-32-or-higher-optional-feature).
- Hỗ trợ tùy chọn SSL/TLS trên cổng điều khiển. Xem [phần dưới](#ssl).
- Tùy chọn STREAM FORWARD với SSL=true

#### Đa luồng

- Cho phép nhiều lệnh STREAM ACCEPT đang chờ xử lý đồng thời trên cùng một ID phiên.

#### Phân tích cú pháp dòng lệnh và Keepalive

- Các lệnh tùy chọn QUIT, STOP và EXIT để đóng phiên và socket. Xem [phía dưới](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- Việc phân tích lệnh sẽ xử lý đúng UTF-8
- Việc phân tích lệnh xử lý đáng tin cậy khoảng trắng bên trong dấu ngoặc kép
- Dấu gạch ngược '\\' có thể dùng để bỏ qua dấu ngoặc kép trên dòng lệnh
- Nên để máy chủ ánh xạ các lệnh thành chữ in hoa, để dễ kiểm thử thông qua telnet.
- Các giá trị tùy chọn rỗng như PROTOCOL hoặc PROTOCOL= có thể được cho phép, tùy theo cách triển khai.
- PING/PONG để duy trì kết nối. Xem phía dưới.
- Máy chủ có thể triển khai thời gian chờ cho lệnh HELLO hoặc các lệnh tiếp theo, tùy theo cách triển khai.

### Thay đổi phiên bản 3.3

Phiên bản 3.3 được giới thiệu trong bản phát hành Java I2P 0.9.25 (tháng 3 năm 2016). Lưu ý rằng i2pd hiện tại không hỗ trợ hầu hết các tính năng của phiên bản 3.3.

- Cùng một phiên có thể được sử dụng đồng thời cho stream, datagram và raw. Các gói tin và stream đến sẽ được định tuyến dựa trên giao thức I2P và cổng đến (to-port). Xem [mục PHIÊN CHÍNH bên dưới](#sam-primary-sessions-v33-and-higher).
- DATAGRAM SEND và RAW SEND hiện hỗ trợ các tùy chọn SEND_TAGS, TAG_THRESHOLD, EXPIRES và SEND_LEASESET. Xem [mục gửi datagram có phản hồi hoặc dạng raw bên dưới](#sending-repliable-or-raw-datagrams).

### Thay đổi tháng 04 năm 2025

Hai đề xuất đã được phê duyệt và tích hợp vào đặc tả tại đây vào tháng 4 năm 2025. Không có sự thay đổi phiên bản nào để chỉ rõ việc hỗ trợ. Một số phần triển khai vẫn chưa hỗ trợ, và ở những phần triển khai khác, việc hỗ trợ vẫn còn ở giai đoạn sơ bộ.

- Hỗ trợ Datagram 2/3 (đề xuất 163). Được chỉ định trong SESSION CREATE và SESSION ADD (subsessions). Xem bên dưới.
- Truy xuất các tùy chọn leaseset (đề xuất 167). Được chỉ định bằng NAMING LOOKUP OPTIONS=true. Xem bên dưới.

## Giao thức phiên bản 3

### Tổng quan đặc tả Phiên bản 3.3 của Giao thức Tin nhắn Nặc danh Đơn giản (SAM)

Ứng dụng khách giao tiếp với cầu nối SAM, cái này xử lý toàn bộ các chức năng I2P (sử dụng [thư viện streaming](/docs/api/streaming) cho các luồng ảo, hoặc trực tiếp dùng [I2CP](/docs/protocol/i2cp) cho các gói tin datagram).

Theo mặc định, giao tiếp giữa client và cầu nối SAM là không được mã hóa và không được xác thực. Cầu nối SAM có thể hỗ trợ các kết nối SSL/TLS; các chi tiết cấu hình và triển khai nằm ngoài phạm vi của đặc tả này. Kể từ SAM 3.2, các tham số xác thực tùy chọn tên người dùng/mật khẩu được hỗ trợ trong quá trình bắt tay ban đầu và có thể được yêu cầu bởi cầu nối.

Các giao tiếp I2P có thể có nhiều hình thức khác nhau:

- [Luồng ảo](/docs/api/streaming)
- [Các datagram có thể trả lời và được xác thực](/docs/specs/datagrams#repliable) (tin nhắn có trường FROM)
- [Các datagram ẩn danh](/docs/specs/datagrams#raw) (tin nhắn ẩn danh thô)
- [Datagram2](/docs/specs/datagrams#datagram2) (định dạng mới có thể trả lời và được xác thực)
- [Datagram3](/docs/specs/datagrams#datagram3) (định dạng mới có thể trả lời nhưng không được xác thực)

Các phiên I2P hỗ trợ truyền thông I2P, và mỗi phiên I2P được liên kết với một địa chỉ (gọi là đích). Một phiên I2P được liên kết với một trong ba loại nêu trên, và không thể thực hiện truyền thông của loại khác, trừ khi sử dụng [phiên CHÍNH (PRIMARY sessions)](#sam-primary-sessions-v33-and-higher).

### Mã hóa và Thoát ký tự

Tất cả các tin nhắn SAM này được gửi trên một dòng duy nhất, kết thúc bằng ký tự xuống dòng (\\n). Trước phiên bản SAM 3.2, chỉ hỗ trợ ASCII 7-bit. Kể từ SAM 3.2, mã hóa phải là UTF-8. Mọi khóa hoặc giá trị được mã hóa bằng UTF-8 đều phải hoạt động.

Định dạng được hiển thị trong đặc tả này bên dưới chỉ nhằm mục đích dễ đọc, và mặc dù hai từ đầu tiên trong mỗi tin nhắn phải giữ nguyên thứ tự cụ thể của chúng, thứ tự các cặp khóa=giá trị có thể thay đổi (ví dụ: "ONE TWO A=B C=D" hoặc "ONE TWO C=D A=B" đều là các cấu trúc hợp lệ). Ngoài ra, giao thức này phân biệt chữ hoa chữ thường. Trong các phần tiếp theo, các ví dụ tin nhắn được đặt trước bởi "->" đối với các tin nhắn do client gửi đến cầu nối SAM, và bởi "<-" đối với các tin nhắn do cầu nối SAM gửi đến client.

Dòng lệnh hoặc phản hồi cơ bản có một trong các dạng sau:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
LỆNH mà không có PHIÊN LỆNH chỉ được hỗ trợ đối với một số lệnh mới trong SAM 3.2.

Các cặp khóa=giá trị phải được phân tách bằng một dấu cách duy nhất. (Kể từ SAM 3.2, cho phép nhiều dấu cách) Giá trị phải được đặt trong dấu ngoặc kép nếu chứa khoảng trắng, ví dụ: key="văn bản giá trị dài". (Trước SAM 3.2, tính năng này hoạt động không ổn định trong một số triển khai)

Trước SAM 3.2, không có cơ chế thoát ký tự. Kể từ SAM 3.2, dấu ngoặc kép có thể được thoát bằng dấu gạch ngược '\\' và một dấu gạch ngược có thể được biểu diễn bằng hai dấu gạch ngược '\\\\'.

### Giá trị trống

Tính đến SAM 3.2, các giá trị tùy chọn trống như KEY, KEY=, hoặc KEY="" có thể được cho phép, tùy thuộc vào cách triển khai.

### Độ nhạy chữ hoa/thường

Giao thức, như đã được quy định, phân biệt chữ hoa chữ thường. Nên nhưng không bắt buộc máy chủ ánh xạ các lệnh thành chữ in hoa để thuận tiện cho việc kiểm thử thông qua telnet. Ví dụ, điều này cho phép lệnh "hello version" hoạt động được. Việc này phụ thuộc vào cách triển khai. Không được ánh xạ các khóa hoặc giá trị thành chữ hoa, vì điều đó sẽ làm hỏng các tùy chọn [I2CP](/docs/protocol/i2cp).

### Thiết lập kết nối SAM

Không thể có bất kỳ giao tiếp SAM nào xảy ra cho đến khi client và bridge đạt được thỏa thuận về phiên bản giao thức, việc này được thực hiện bằng cách client gửi một tin nhắn HELLO và bridge phản hồi bằng tin nhắn HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
và

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
Kể từ phiên bản 3.1 (I2P 0.9.14), các tham số MIN và MAX là tùy chọn. SAM sẽ luôn trả về phiên bản cao nhất có thể dựa trên các ràng buộc MIN và MAX, hoặc phiên bản máy chủ hiện tại nếu không có ràng buộc nào được đưa ra.

Nếu cầu nối SAM không thể tìm thấy phiên bản phù hợp, nó sẽ phản hồi bằng:

```
<- HELLO REPLY RESULT=NOVERSION
```
Nếu xảy ra lỗi, ví dụ như định dạng yêu cầu không hợp lệ, nó sẽ phản hồi bằng:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

Socket điều khiển của máy chủ có thể tùy chọn hỗ trợ SSL/TLS, tùy theo cấu hình trên máy chủ và máy khách. Các triển khai cũng có thể cung cấp các lớp truyền tải khác; điều này nằm ngoài phạm vi định nghĩa giao thức.

#### Xác thực

Để xác thực, client thêm USER="xxx" PASSWORD="yyy" vào các tham số HELLO. Nên sử dụng dấu ngoặc kép cho tên người dùng và mật khẩu, nhưng không bắt buộc. Nếu có dấu ngoặc kép bên trong tên người dùng hoặc mật khẩu, cần thêm dấu gạch ngược để thoát. Khi thất bại, máy chủ sẽ phản hồi bằng I2P_ERROR cùng một thông báo. Nên bật SSL trên mọi máy chủ SAM nơi yêu cầu xác thực.

#### Thời gian chờ

Các máy chủ có thể triển khai thời gian chờ cho lệnh HELLO hoặc các lệnh tiếp theo, tùy thuộc vào cách triển khai. Máy khách nên gửi nhanh lệnh HELLO và lệnh tiếp theo ngay sau khi kết nối.

Nếu xảy ra hết thời gian chờ trước khi nhận được HELLO, cầu nối sẽ phản hồi bằng:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
và sau đó ngắt kết nối.

Nếu thời gian chờ hết hạn sau khi nhận được HELLO nhưng trước lệnh tiếp theo, cầu nối sẽ phản hồi bằng:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
và sau đó ngắt kết nối.

### Cổng và Giao thức I2CP

Kể từ SAM 3.2, các cổng và giao thức [I2CP](/docs/protocol/i2cp) có thể được gửi bởi máy khách SAM để truyền qua [I2CP](/docs/protocol/i2cp), và cầu nối SAM sẽ truyền thông tin cổng và giao thức [I2CP](/docs/protocol/i2cp) nhận được tới máy khách SAM.

Đối với FROM_PORT và TO_PORT, phạm vi hợp lệ là 0-65535, và giá trị mặc định là 0.

Đối với PROTOCOL, chỉ có thể được chỉ định cho RAW, phạm vi hợp lệ là 0-255, và giá trị mặc định là 18.

Đối với các lệnh SESSION, các cổng và giao thức được chỉ định là giá trị mặc định cho phiên đó. Đối với các luồng hoặc datagram riêng lẻ, các cổng và giao thức được chỉ định sẽ ghi đè các giá trị mặc định của phiên. Đối với các luồng hoặc datagram được nhận, các cổng và giao thức được chỉ ra là như đã nhận từ [I2CP](/docs/protocol/i2cp).

#### Sự khác biệt quan trọng so với IP tiêu chuẩn

Các cổng I2CP dùng cho socket và datagram I2P. Chúng không liên quan đến các socket cục bộ của bạn kết nối tới SAM.

- Cổng 0 là hợp lệ và có ý nghĩa đặc biệt.
- Các cổng 1-1023 không đặc biệt hay được cấp quyền đặc biệt.
- Máy chủ mặc định lắng nghe trên cổng 0, có nghĩa là "tất cả các cổng".
- Máy khách mặc định gửi đến cổng 0, có nghĩa là "bất kỳ cổng nào".
- Máy khách mặc định gửi từ cổng 0, có nghĩa là "chưa xác định".
- Máy chủ có thể có một dịch vụ lắng nghe trên cổng 0 và các dịch vụ khác lắng nghe trên các cổng cao hơn. Trong trường hợp đó, dịch vụ cổng 0 là mặc định và sẽ được kết nối nếu cổng socket hoặc datagram đầu vào không khớp với dịch vụ nào khác.
- Hầu hết các điểm đến I2P chỉ chạy một dịch vụ, do đó bạn có thể sử dụng các giá trị mặc định và bỏ qua cấu hình cổng I2CP.
- Cần dùng SAM 3.2 hoặc 3.3 để chỉ định cổng I2CP.
- Nếu bạn không cần chỉ định cổng I2CP, thì bạn không cần SAM 3.2 hay 3.3; SAM 3.1 là đủ.
- Giao thức 0 là hợp lệ và có nghĩa là "bất kỳ giao thức nào". Tuy nhiên điều này không được khuyến khích và có thể sẽ không hoạt động.
- Các socket I2P được theo dõi thông qua một ID kết nối nội bộ. Do đó, không yêu cầu 5-tuple gồm dest:port:dest:port:protocol phải là duy nhất. Ví dụ, có thể có nhiều socket với cùng cổng giữa hai điểm đến. Máy khách không cần phải chọn "cổng trống" cho một kết nối đi ra.

Nếu bạn đang thiết kế một ứng dụng SAM 3.3 với nhiều phiên con, hãy cân nhắc kỹ cách sử dụng các cổng và giao thức một cách hiệu quả. Xem đặc tả [I2CP](/docs/protocol/i2cp) để biết thêm thông tin.

### Phiên SAM

Một phiên SAM được tạo ra khi một client mở một socket đến cầu nối SAM, thực hiện quá trình bắt tay và gửi tin nhắn SESSION CREATE, và phiên sẽ kết thúc khi socket bị ngắt kết nối.

Mỗi Điểm đến I2P đã đăng ký được liên kết duy nhất với một ID phiên (hoặc biệt danh). Các ID phiên, bao gồm cả ID phiên phụ cho các phiên CHÍNH, phải là duy nhất trên toàn bộ máy chủ SAM. Để tránh khả năng trùng lặp ID với các máy khách khác, cách làm tốt nhất là máy khách nên tạo các ID một cách ngẫu nhiên.

Mỗi phiên được liên kết duy nhất với:

- socket mà client dùng để tạo phiên
- ID (hoặc biệt danh) của nó

#### Yêu cầu tạo phiên

Tin nhắn tạo phiên chỉ có thể sử dụng một trong các dạng này (các tin nhắn nhận được qua dạng khác sẽ được trả lời bằng thông báo lỗi):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION xác định đích sẽ được sử dụng để gửi và nhận các tin nhắn/dòng dữ liệu. Giá trị $privkey là dạng base 64 của chuỗi nối giữa [Destination](/docs/specs/common-structures#type_Destination), [Private Key](/docs/specs/common-structures#type_PrivateKey) và [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), tùy chọn có thể thêm phần [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), với độ dài tối thiểu 663 byte ở dạng nhị phân hoặc 884 byte ở dạng base 64, tùy theo loại chữ ký. Định dạng nhị phân được mô tả trong phần Private Key File. Xem thêm ghi chú về [Private Key](/docs/specs/common-structures#type_PrivateKey) trong phần tạo khóa Destination bên dưới.

Nếu khóa riêng dùng để ký toàn bộ là số không, thì phần [Chữ ký ngoại tuyến](/docs/specs/common-structures#struct_OfflineSignature) sẽ được đưa ra. Chữ ký ngoại tuyến chỉ được hỗ trợ cho các phiên STREAM và RAW. Chữ ký ngoại tuyến không được tạo với DESTINATION=TRANSIENT. Định dạng của phần chữ ký ngoại tuyến như sau:

1. Thời điểm hết hạn (4 byte, big endian, số giây kể từ thời điểm khởi tạo, tràn vào năm 2106)
2. Loại chữ ký của Khóa công khai ký tạm thời (2 byte, big endian)
3. Khóa công khai ký tạm thời (độ dài theo quy định bởi loại chữ ký tạm thời)
4. Chữ ký của ba trường trên do khóa ngoại tuyến tạo (độ dài theo quy định bởi loại chữ ký đích)
5. Khóa riêng ký tạm thời (độ dài theo quy định bởi loại chữ ký tạm thời)

Nếu đích được chỉ định là TRANSIENT, cầu nối SAM sẽ tạo một đích mới. Kể từ phiên bản 3.1 (I2P 0.9.14), nếu đích là TRANSIENT, tham số tùy chọn SIGNATURE_TYPE được hỗ trợ. Giá trị SIGNATURE_TYPE có thể là bất kỳ tên nào (ví dụ: ECDSA_SHA256_P256, không phân biệt chữ hoa/thường) hoặc số (ví dụ: 1) được hỗ trợ bởi [Chứng chỉ khóa](/docs/specs/common-structures#type_Certificate). Giá trị mặc định là DSA_SHA1, điều này KHÔNG PHẢI là thứ bạn muốn. Đối với hầu hết các ứng dụng, vui lòng chỉ định SIGNATURE_TYPE=7.

$nickname là lựa chọn của khách hàng. Không được phép có khoảng trắng.

Các tùy chọn bổ sung được cung cấp sẽ được truyền vào cấu hình phiên I2P nếu không được cầu SAM diễn giải (ví dụ: outbound.length=0).

Các bộ định tuyến Java I2P và i2pd có giá trị mặc định khác nhau về số lượng tunnel. Giá trị mặc định của Java là 2 và của i2pd là 5. Đối với hầu hết các trường hợp có băng thông thấp đến trung bình và số lượng kết nối thấp đến trung bình, con số 2 hoặc 3 là đủ. Vui lòng chỉ định số lượng tunnel trong tin nhắn SESSION CREATE để có hiệu suất ổn định khi dùng với các bộ định tuyến Java I2P và i2pd, bằng cách sử dụng các tùy chọn như ví dụ: inbound.quantity=3 outbound.quantity=3. Các tùy chọn này và một số khác [được ghi chú chi tiết trong các liên kết bên dưới](#tunnel-i2cp-and-streaming-options).

Bản thân cầu nối SAM đã phải được cấu hình sẵn để giao tiếp qua I2P thông qua router nào (mặc dù nếu cần, có thể có cách để ghi đè, ví dụ như i2cp.tcp.host=localhost và i2cp.tcp.port=7654).

#### Phản hồi Tạo phiên

Sau khi nhận được tin nhắn tạo phiên, cầu nối SAM sẽ phản hồi bằng một tin nhắn trạng thái phiên, như sau:

Nếu việc tạo thành công:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey là dạng base 64 của chuỗi nối [Destination](/docs/specs/common-structures#type_Destination), tiếp theo là [Private Key](/docs/specs/common-structures#type_PrivateKey), rồi đến [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), và tùy chọn có thể thêm [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), với độ dài tối thiểu 663 byte ở dạng nhị phân hoặc 884 byte ở dạng base 64, tùy theo loại chữ ký. Định dạng nhị phân được mô tả trong tài liệu Private Key File.

Nếu SESSION CREATE chứa khóa riêng để ký gồm toàn số không và một phần [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), phản hồi SESSION STATUS sẽ bao gồm dữ liệu tương tự theo cùng định dạng. Xem phần SESSION CREATE ở trên để biết chi tiết.

Nếu biệt danh đã được liên kết với một phiên:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Nếu đích đến đã được sử dụng:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Nếu đích đến không phải là khóa đích riêng hợp lệ:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Nếu một lỗi khác xảy ra:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Nếu không ổn, MESSAGE nên chứa thông tin dễ đọc giải thích lý do tại sao phiên không thể được tạo.

Lưu ý rằng bộ định tuyến sẽ xây dựng các đường hầm trước khi phản hồi bằng SESSION STATUS. Việc này có thể mất vài giây, hoặc trong trường hợp khởi động bộ định tuyến hoặc tắc nghẽn mạng nghiêm trọng, có thể mất một phút trở lên. Nếu không thành công, bộ định tuyến sẽ không phản hồi với thông báo lỗi trong vài phút. Không nên đặt thời gian chờ ngắn khi đợi phản hồi. Không nên từ bỏ phiên làm việc trong khi việc xây dựng đường hầm đang diễn ra và thử lại.

Các phiên SAM tồn tại và chấm dứt cùng với socket mà chúng được liên kết. Khi socket bị đóng, phiên sẽ chấm dứt, và mọi kết nối sử dụng phiên đó cũng đồng thời ngừng hoạt động. Và ngược lại, khi phiên chấm dứt vì bất kỳ lý do gì, cầu nối SAM sẽ đóng socket.

### SAM Virtual Streams

Các luồng ảo được đảm bảo gửi một cách đáng tin cậy và theo đúng thứ tự, với thông báo lỗi hoặc thành công ngay khi có thể.

Các stream là các ổ cắm giao tiếp hai chiều giữa hai điểm đến I2P, nhưng việc mở stream phải do một trong hai bên yêu cầu. Sau đây, các lệnh CONNECT được sử dụng bởi client SAM để gửi yêu cầu đó. Các lệnh FORWARD / ACCEPT được sử dụng bởi client SAM khi nó muốn lắng nghe các yêu cầu đến từ các điểm đến I2P khác.

### Luồng ảo SAM: KẾT NỐI

Một client yêu cầu kết nối bằng cách:

- mở một socket mới với cầu nối SAM
- truyền cùng bản chào tay HELLO như trên
- gửi lệnh STREAM CONNECT

#### Yêu cầu kết nối

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Thiết lập một kết nối ảo mới từ phiên cục bộ có ID là $nickname đến máy ngang hàng được chỉ định.

Đích đến là $destination, chính là chuỗi cơ số 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự cơ số 64 trở lên (tương đương 387 byte trở lên ở dạng nhị phân), tùy thuộc vào loại chữ ký.

**LƯU Ý:** Kể từ khoảng năm 2014 (SAM v3.1), Java I2P cũng đã hỗ trợ tên miền và địa chỉ b32 cho $destination, nhưng trước đây thông tin này chưa được tài liệu hóa. Tên miền và địa chỉ b32 hiện đã được Java I2P chính thức hỗ trợ kể từ phiên bản 0.9.48. Router i2pd hỗ trợ tên miền và địa chỉ b32 kể từ phiên bản 2.38.0 (0.9.50). Với cả hai router, việc hỗ trợ "b32" bao gồm cả hỗ trợ địa chỉ "b33" mở rộng dành cho các đích ẩn danh (blinded destinations).

#### Phản hồi kết nối

Nếu SILENT=true được thiết lập, cầu nối SAM sẽ không gửi bất kỳ thông báo nào khác qua socket. Nếu kết nối thất bại, socket sẽ bị đóng. Nếu kết nối thành công, toàn bộ dữ liệu còn lại đi qua socket hiện tại sẽ được chuyển tiếp từ và đến điểm đến I2P đã kết nối.

Nếu SILENT=false, đây là giá trị mặc định, cầu nối SAM sẽ gửi một tin nhắn cuối cùng đến máy khách của nó trước khi chuyển tiếp hoặc tắt kết nối socket:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Nếu KẾT QUẢ là OK, toàn bộ dữ liệu còn lại đi qua socket hiện tại sẽ được chuyển tiếp tới và từ điểm đồng đẳng I2P đích đã kết nối. Nếu việc kết nối không thể thực hiện được (hết thời gian chờ, v.v.), KẾT QUẢ sẽ chứa giá trị lỗi phù hợp (kèm theo thông điệp MESSAGE có thể đọc được bởi con người, nếu có), và cầu nối SAM sẽ đóng socket lại.

Thời gian chờ kết nối luồng của bộ định tuyến bên trong khoảng một phút, tùy thuộc vào cách triển khai. Không đặt thời gian chờ ngắn hơn khi chờ phản hồi.

### SAM Virtual Streams: CHẤP NHẬN

Một máy khách chờ yêu cầu kết nối đến bằng cách:

- mở một socket mới với cầu nối SAM
- truyền cùng handshake HELLO như trên
- gửi lệnh STREAM ACCEPT

#### Chấp nhận yêu cầu

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Điều này khiến phiên ${nickname} lắng nghe một yêu cầu kết nối đến từ mạng I2P. ACCEPT không được phép khi có một lệnh FORWARD đang hoạt động trên phiên.

Kể từ SAM 3.2, việc chấp nhận đồng thời nhiều yêu cầu STREAM đang chờ xử lý trên cùng một ID phiên (thậm chí với cùng một cổng) là được phép. Trước phiên bản 3.2, các yêu cầu chấp nhận đồng thời sẽ thất bại với lỗi ALREADY_ACCEPTING. Ghi chú: Java I2P cũng hỗ trợ việc chấp nhận đồng thời trên SAM 3.1, kể từ phiên bản 0.9.24 (2016-01). i2pd cũng hỗ trợ việc chấp nhận đồng thời trên SAM 3.1, kể từ phiên bản 2.50.0 (2023-12).

#### Chấp nhận Phản hồi

Nếu SILENT=true được thiết lập, cầu nối SAM sẽ không gửi bất kỳ thông báo nào khác qua socket. Nếu việc chấp nhận kết nối thất bại, socket sẽ bị đóng. Nếu việc chấp nhận kết nối thành công, toàn bộ dữ liệu còn lại đi qua socket hiện tại sẽ được chuyển tiếp từ và đến điểm đến I2P đã kết nối. Để đảm bảo độ tin cậy và để nhận được địa chỉ đích cho các kết nối đến, nên đặt SILENT=false.

Nếu SILENT=false, đây là giá trị mặc định, cầu nối SAM sẽ trả lời bằng:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

```
OK
I2P_ERROR
INVALID_ID
```
Nếu kết quả không phải là OK, socket sẽ bị đóng ngay lập tức bởi cầu nối SAM. Nếu kết quả là OK, cầu nối SAM sẽ bắt đầu chờ yêu cầu kết nối đến từ một peer I2P khác. Khi yêu cầu đến, cầu nối SAM sẽ chấp nhận nó và:

Nếu SILENT=true được truyền vào, cầu nối SAM sẽ không gửi bất kỳ thông báo nào khác qua socket của client. Tất cả dữ liệu còn lại đi qua socket hiện tại sẽ được chuyển tiếp từ và đến peer đích I2P đã kết nối.

Nếu SILENT=false được truyền vào, đây là giá trị mặc định, cầu nối SAM sẽ gửi cho client một dòng ASCII chứa khóa công khai dạng base64 của điểm ngang hàng đang yêu cầu, và thông tin bổ sung chỉ dành cho SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Sau dòng kết thúc bằng '\\n' này, toàn bộ dữ liệu còn lại đi qua cổng kết nối hiện tại sẽ được chuyển tiếp từ và đến điểm đồng đẳng I2P đích đã kết nối, cho đến khi một trong hai điểm đồng đẳng đóng cổng kết nối.

#### Lỗi sau OK

Trong một số trường hợp hiếm gặp, cầu nối SAM có thể gặp lỗi sau khi gửi RESULT=OK, nhưng trước khi một kết nối được thiết lập và gửi dòng $destination đến client. Các lỗi này có thể bao gồm việc router tắt, khởi động lại router, hoặc đóng phiên. Trong những trường hợp này, khi SILENT=false, cầu nối SAM có thể (nhưng không bắt buộc — tùy theo cách triển khai) gửi dòng:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
trước khi đóng ngay lập tức kết nối socket. Dòng này tất nhiên không thể giải mã thành một đích Base 64 hợp lệ.

### Luồng ảo SAM: CHUYỂN TIẾP

Một máy khách có thể sử dụng máy chủ socket thông thường và chờ các yêu cầu kết nối đến từ I2P. Để làm được điều đó, máy khách phải:

- mở một socket mới với cầu nối SAM
- gửi handshake HELLO giống như ở trên
- gửi lệnh chuyển tiếp (forward command)

#### Yêu cầu chuyển tiếp

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Điều này khiến phiên ${nickname} lắng nghe các yêu cầu kết nối đến từ mạng I2P. KHÔNG được phép chuyển tiếp (FORWARD) khi vẫn còn một yêu cầu CHẤP NHẬN (ACCEPT) đang chờ xử lý trên phiên.

#### Phản hồi chuyển tiếp

SILENT mặc định là false. Cho dù SILENT là true hay false, cầu nối SAM luôn trả lời bằng thông điệp STREAM STATUS. Lưu ý rằng đây là hành vi khác với STREAM ACCEPT và STREAM CONNECT khi SILENT=true. Thông điệp STREAM STATUS là:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Giá trị RESULT có thể là một trong các giá trị sau:

```
OK
I2P_ERROR
INVALID_ID
```
$host là tên máy hoặc địa chỉ IP của máy chủ socket mà SAM sẽ chuyển tiếp các yêu cầu kết nối đến. Nếu không được cung cấp, SAM sẽ lấy địa chỉ IP của socket đã gửi lệnh chuyển tiếp.

$port là số cổng của máy chủ socket mà SAM sẽ chuyển tiếp các yêu cầu kết nối đến. Bắt buộc phải có.

Khi một yêu cầu kết nối đến từ I2P, cầu nối SAM sẽ mở một kết nối socket đến $host:$port. Nếu kết nối được chấp nhận trong vòng chưa đầy 3 giây, SAM sẽ chấp nhận kết nối từ I2P, và sau đó:

Nếu SILENT=true được thiết lập, mọi dữ liệu đi qua cổng socket hiện tại thu được sẽ được chuyển tiếp từ và đến máy ngang hàng I2P đích đã kết nối.

Nếu SILENT=false được truyền vào, đây là giá trị mặc định, cầu nối SAM sẽ gửi qua socket đã nhận được một dòng ASCII chứa khóa công khai dạng base64 của điểm đích từ máy ngang hàng yêu cầu, và thêm thông tin dành riêng cho SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Sau dòng kết thúc bằng '\\n' này, tất cả dữ liệu còn lại đi qua socket sẽ được chuyển tiếp từ và đến điểm đích I2P đã kết nối, cho đến khi một trong hai phía đóng socket.

Kể từ SAM 3.2, nếu chỉ định SSL=true, socket chuyển tiếp sẽ sử dụng SSL/TLS.

Bộ định tuyến I2P sẽ ngừng lắng nghe các yêu cầu kết nối đến ngay khi cổng "forwarding" bị đóng.

### SAM Datagrams

SAMv3 cung cấp các cơ chế để gửi và nhận các gói tin qua các ổ cắm giao thức datagram cục bộ. Một số triển khai SAMv3 cũng hỗ trợ phương thức cũ v1/v2 để gửi/nhận các gói tin qua ổ cắm cầu nối SAM. Cả hai phương thức đều được mô tả bên dưới.

I2P hỗ trợ bốn loại datagram:

- Các gói tin có thể trả lời và được xác thực được đặt trước bằng đích của người gửi, và chứa chữ ký của người gửi, để người nhận có thể xác minh rằng đích của người gửi không bị giả mạo, và có thể phản hồi lại gói tin. Định dạng Datagram2 mới cũng có khả năng trả lời và được xác thực.
- Định dạng Datagram3 mới có thể trả lời nhưng không được xác thực. Thông tin người gửi không được xác minh.
- Các gói tin thô (raw datagrams) không chứa đích của người gửi cũng như chữ ký nào.

Các cổng I2CP mặc định được xác định cho cả datagram có thể trả lời và datagram thô. Cổng I2CP có thể được thay đổi đối với datagram thô.

Một mẫu thiết kế giao thức phổ biến là việc gửi các gói tin có thể trả lời đến máy chủ, kèm theo một định danh nào đó, và máy chủ sẽ phản hồi bằng một gói tin thô chứa định danh này, để phản hồi có thể được liên kết với yêu cầu. Mẫu thiết kế này loại bỏ phần lớn chi phí phát sinh do việc sử dụng các gói tin có thể trả lời trong phản hồi. Tất cả các lựa chọn về giao thức và cổng I2CP đều phụ thuộc vào từng ứng dụng cụ thể, và các nhà thiết kế cần cân nhắc những vấn đề này.

Xem thêm các ghi chú quan trọng về MTU của datagram trong phần bên dưới.

#### Gửi các gói tin có thể trả lời hoặc gói tin thô

Mặc dù I2P không chứa địa chỉ GỬI (FROM) theo cách vốn có, nhưng để thuận tiện khi sử dụng, một lớp bổ sung được cung cấp dưới dạng các gói dữ liệu có thể trả lời (repliable datagrams) – những tin nhắn không theo thứ tự và không đảm bảo tin cậy, với kích thước tối đa 31744 byte, bao gồm địa chỉ GỬI (để lại tối đa 1KB cho phần tiêu đề). Địa chỉ GỬI này được xác thực nội bộ bởi SAM (tận dụng khóa ký của đích để xác minh nguồn) và bao gồm cơ chế ngăn chặn việc phát lại (replay prevention).

Kích thước tối thiểu là 1. Để đảm bảo độ tin cậy truyền tải tốt nhất, kích thước tối đa được khuyến nghị là khoảng 11 KB. Độ tin cậy giảm dần khi kích thước tin nhắn tăng lên, có thể theo cấp số mũ.

Sau khi thiết lập phiên SAM với STYLE=DATAGRAM hoặc STYLE=RAW, máy khách có thể gửi các datagram có thể trả lời (repliable) hoặc datagram thô thông qua cổng UDP của SAM (mặc định là 7655).

Dòng đầu tiên của một datagram được gửi qua cổng này phải có định dạng như sau. Tất cả nằm trên một dòng (các phần cách nhau bằng dấu cách), được hiển thị trên nhiều dòng để dễ hiểu:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 là phiên bản của SAM. Kể từ SAM 3.2, mọi phiên bản 3.x đều được cho phép.
- $nickname là ID của phiên DATAGRAM sẽ được sử dụng
- Mục tiêu là $destination, chính là dạng base 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự base 64 hoặc hơn (387 byte hoặc nhiều hơn ở dạng nhị phân), tùy theo loại chữ ký. **LƯU Ý:** Từ khoảng năm 2014 (SAM v3.1), Java I2P cũng hỗ trợ tên miền và địa chỉ b32 cho $destination, nhưng trước đây tính năng này chưa được tài liệu hóa. Tên miền và địa chỉ b32 hiện đã được Java I2P hỗ trợ chính thức kể từ phiên bản 0.9.48. Trình định tuyến i2pd hiện tại không hỗ trợ tên miền và địa chỉ b32; tính năng này có thể được thêm vào trong các phiên bản tương lai.
- Tất cả các tùy chọn đều là thiết lập riêng cho từng datagram, ghi đè lên các giá trị mặc định được chỉ định trong SESSION CREATE.
- Các tùy chọn phiên bản 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES và SEND_LEASESET sẽ được truyền tới [I2CP](/docs/protocol/i2cp) nếu được hỗ trợ. Xem [đặc tả I2CP](/docs/protocol/i2cp#msg_SendMessageExpire) để biết chi tiết. Việc hỗ trợ các tùy chọn này bởi máy chủ SAM là tùy chọn, và sẽ bỏ qua nếu không được hỗ trợ.
- dòng này kết thúc bằng '\\n'.

Dòng đầu tiên sẽ bị SAM loại bỏ trước khi gửi phần dữ liệu còn lại của tin nhắn đến đích đã chỉ định.

Đối với phương pháp thay thế để gửi các gói tin có thể trả lời và gói tin thô, hãy xem [DATAGRAM SEND và RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### SAM Repliable Datagrams: Nhận một Datagram

Các gói dữ liệu nhận được sẽ được SAM ghi vào socket mà phiên gói dữ liệu được mở từ đó, nếu không chỉ định cổng chuyển tiếp (PORT) trong lệnh SESSION CREATE. Đây là cách tương thích với v1/v2 để nhận các gói dữ liệu.

Khi một gói dữ liệu đến, cầu nối sẽ chuyển tiếp nó đến máy khách thông qua tin nhắn:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
Nguồn là $destination, chính là dạng base 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự base 64 hoặc nhiều hơn (387 byte hoặc nhiều hơn ở dạng nhị phân), tùy thuộc vào loại chữ ký.

Cầu nối SAM không bao giờ tiết lộ cho máy khách các tiêu đề xác thực hoặc các trường khác, mà chỉ cung cấp dữ liệu mà người gửi đã gửi. Điều này tiếp tục cho đến khi phiên làm việc được đóng lại (khi máy khách ngắt kết nối).

#### Chuyển tiếp các gói tin thô hoặc gói tin có thể trả lời được

Khi tạo một phiên datagram, client có thể yêu cầu SAM chuyển tiếp các tin nhắn đến tới một địa chỉ ip:port đã chỉ định. Để làm điều này, client gửi lệnh CREATE kèm các tùy chọn PORT và HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey là dạng base 64 của chuỗi nối giữa [Destination](/docs/specs/common-structures#type_Destination), tiếp theo là [Private Key](/docs/specs/common-structures#type_PrivateKey), rồi đến [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), và tùy chọn có thể thêm [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), với tổng chiều dài tối thiểu 884 ký tự base 64 (tương đương 663 byte hoặc nhiều hơn ở dạng nhị phân), tùy thuộc vào loại chữ ký. Định dạng nhị phân được mô tả trong tài liệu Private Key File.

Chữ ký ngoại tuyến được hỗ trợ cho các gói tin RAW, DATAGRAM2 và DATAGRAM3, nhưng không hỗ trợ cho DATAGRAM. Xem phần SESSION CREATE ở trên và phần DATAGRAM2/3 ở dưới để biết chi tiết.

$host là tên miền hoặc địa chỉ IP của máy chủ datagram mà SAM sẽ chuyển tiếp các datagram đến. Nếu không được cung cấp, SAM sẽ lấy địa chỉ IP của socket đã gửi lệnh chuyển tiếp.

$port là số cổng của máy chủ datagram mà SAM sẽ chuyển tiếp các datagram đến. Nếu $port không được thiết lập, các datagram sẽ KHÔNG được chuyển tiếp, mà sẽ được nhận trên socket điều khiển theo cách tương thích với v1/v2.

Các tùy chọn bổ sung được cung cấp sẽ được chuyển đến cấu hình phiên I2P nếu không được cầu SAM diễn giải (ví dụ: outbound.length=0). Các tùy chọn này [được mô tả bên dưới](#tunnel-i2cp-and-streaming-options).

Các datagram có thể trả lời được chuyển tiếp luôn được tiền tố bằng đích base64, ngoại trừ Datagram3, xem bên dưới. Khi một datagram có thể trả lời đến, cầu nối sẽ gửi đến host:port đã chỉ định một gói UDP chứa dữ liệu sau:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Các gói tin datagram thô được chuyển tiếp sẽ được gửi nguyên trạng đến host:port đã chỉ định mà không có tiền tố. Gói tin UDP chứa dữ liệu sau:

```
$datagram_payload
```
Kể từ SAM 3.2, khi HEADER=true được chỉ định trong SESSION CREATE, datagram thô được chuyển tiếp sẽ được thêm vào đầu một dòng tiêu đề như sau:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination là dạng base 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự base 64 hoặc nhiều hơn (387 byte hoặc nhiều hơn ở dạng nhị phân), tùy thuộc vào loại chữ ký.

#### SAM Datagram Ẩn danh (Nguyên bản)

Tận dụng tối đa băng thông của I2P, SAM cho phép các máy khách gửi và nhận các gói tin vô danh, việc xác thực và thông tin phản hồi do chính máy khách tự xử lý. Các gói tin này không đảm bảo độ tin cậy và thứ tự, và có thể dài tới 32768 byte.

Kích thước tối thiểu là 1. Để đảm bảo độ tin cậy giao hàng tốt nhất, kích thước tối đa được khuyến nghị là khoảng 11 KB.

Sau khi thiết lập phiên SAM với STYLE=RAW, client có thể gửi các datagram ẩn danh thông qua cầu nối SAM giống hệt như cách [gửi các datagram có thể trả lời](#sending-repliable-or-raw-datagrams).

Cả hai cách nhận datagram đều khả dụng cho các datagram ẩn danh.

Các gói dữ liệu nhận được sẽ được SAM ghi vào socket mà phiên gói dữ liệu được mở từ đó, nếu không chỉ định cổng chuyển tiếp (PORT) trong lệnh SESSION CREATE. Đây là cách tương thích với v1/v2 để nhận các gói dữ liệu.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Khi các datagram ẩn danh cần được chuyển tiếp đến một máy chủ:cổng nào đó, cầu nối sẽ gửi đến máy chủ:cổng đã chỉ định một tin nhắn chứa dữ liệu sau:

```
$datagram_payload
```
Kể từ SAM 3.2, khi HEADER=true được chỉ định trong SESSION CREATE, datagram thô được chuyển tiếp sẽ được thêm vào đầu một dòng tiêu đề như sau:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Để biết phương pháp thay thế khác nhằm gửi các gói dữ liệu ẩn danh, hãy xem [GỬI RAW](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Gói tin 2/3

Datagram 2/3 là các định dạng mới được quy định vào đầu năm 2025. Hiện tại chưa có triển khai nào được biết đến. Hãy kiểm tra tài liệu triển khai để biết trạng thái hiện tại. Xem [đặc tả](/docs/specs/datagrams) để biết thêm thông tin.

Hiện tại không có kế hoạch nào để tăng phiên bản SAM nhằm xác định việc hỗ trợ Datagram 2/3. Điều này có thể gây vấn đề vì các triển khai có thể muốn hỗ trợ Datagram 2/3 nhưng không hỗ trợ các tính năng của SAM v3.3. Việc thay đổi phiên bản (nếu có) sẽ được thông báo sau (TBD).

Cả Datagram2 và Datagram3 đều có thể trả lời được. Chỉ có Datagram2 là được xác thực.

Datagram2 giống hệt với các datagram có thể trả lời được về mặt SAM. Cả hai đều được xác thực. Chỉ định dạng I2CP và chữ ký là khác nhau, nhưng điều này không hiển thị với các client SAM. Datagram2 cũng hỗ trợ chữ ký ngoại tuyến, do đó nó có thể được sử dụng bởi các đích có chữ ký ngoại tuyến.

Mục đích là để Datagram2 thay thế các datagram có thể trả lời (Repliable datagrams) trong các ứng dụng mới mà không cần tương thích ngược. Datagram2 cung cấp khả năng bảo vệ chống phát lại (replay protection) mà các datagram có thể trả lời không có. Nếu yêu cầu tương thích ngược, một ứng dụng có thể hỗ trợ cả Datagram2 và Repliable trên cùng một phiên, sử dụng phiên PRIMARY của SAM 3.3.

Datagram3 có thể trả lời nhưng không được xác thực. Trường 'from' trong định dạng I2CP là một mã băm, chứ không phải đích đến. $destination khi được gửi từ máy chủ SAM đến máy khách sẽ là một mã băm base64 dài 44 byte. Để chuyển đổi nó thành một đích đến đầy đủ nhằm trả lời, hãy giải mã base64 thành 32 byte dữ liệu nhị phân, sau đó mã hóa base32 để được chuỗi 52 ký tự và thêm vào hậu tố ".b32.i2p" để thực hiện tra cứu tên (NAMING LOOKUP). Như thường lệ, các máy khách nên tự duy trì bộ nhớ đệm để tránh việc lặp lại các lần tra cứu tên.

Các nhà thiết kế ứng dụng nên hết sức thận trọng và cân nhắc các hệ quả về bảo mật của các gói tin không được xác thực.

#### Các cân nhắc về MTU Datagram V3

Các gói tin I2P có thể lớn hơn MTU điển hình của internet là 1500. Các gói tin gửi cục bộ và các gói tin chuyển tiếp có thể trả lời được, được thêm tiền tố là đích base64 dài 516 byte trở lên, có khả năng vượt quá MTU này. Tuy nhiên, các MTU localhost trên hệ thống Linux thường lớn hơn nhiều, ví dụ như 65536. MTU localhost sẽ khác nhau tùy theo hệ điều hành. Các gói tin I2P sẽ không bao giờ lớn hơn 65536. Kích thước gói tin phụ thuộc vào giao thức ứng dụng.

Nếu máy khách SAM nằm cùng địa phương với máy chủ SAM và hệ thống hỗ trợ MTU lớn hơn, thì các datagram sẽ không bị phân mảnh tại chỗ. Tuy nhiên, nếu máy khách SAM ở xa, thì các datagram IPv4 sẽ bị phân mảnh và các datagram IPv6 sẽ thất bại (IPv6 không hỗ trợ phân mảnh UDP).

Các nhà phát triển thư viện và ứng dụng khách nên biết những vấn đề này và tài liệu hóa các khuyến nghị để tránh phân mảnh và ngăn ngừa mất gói tin, đặc biệt là trên các kết nối từ xa giữa máy khách và máy chủ SAM.

#### GỬI DATAGRAM, GỬI THÔ (Xử lý Datagram tương thích V1/V2)

Trong SAM V3, cách được ưu tiên để gửi các datagram là thông qua cổng socket datagram tại cổng 7655 như đã mô tả ở trên. Tuy nhiên, các datagram có thể trả lời được có thể được gửi trực tiếp thông qua socket cầu nối SAM bằng lệnh DATAGRAM SEND, như được mô tả trong [SAM V1](/docs/api/sam) và [SAM V2](/docs/api/samv2).

Kể từ phiên bản 0.9.14 (phiên bản 3.1), các gói tin vô danh có thể được gửi trực tiếp thông qua cổng nối SAM bằng lệnh RAW SEND, như được mô tả trong [SAM V1](/docs/api/sam) và [SAM V2](/docs/api/samv2).

Kể từ phiên bản phát hành 0.9.24 (phiên bản 3.2), DATAGRAM SEND và RAW SEND có thể bao gồm các tham số FROM_PORT=nnnn và/hoặc TO_PORT=nnnn để ghi đè các cổng mặc định. Kể từ phiên bản phát hành 0.9.24 (phiên bản 3.2), RAW SEND có thể bao gồm tham số PROTOCOL=nnn để ghi đè giao thức mặc định.

Các lệnh này *không* hỗ trợ tham số ID. Các gói tin được gửi đến phiên làm việc kiểu DATAGRAM hoặc RAW được tạo gần đây nhất, tùy theo trường hợp. Hỗ trợ tham số ID có thể được thêm vào trong một phiên bản tương lai.

Các định dạng DATAGRAM2 và DATAGRAM3 *không* được hỗ trợ theo cách tương thích với V1/V2.

### Phiên SAM CHÍNH (V3.3 trở lên)

*Phiên bản 3.3 được giới thiệu trong bản phát hành I2P 0.9.25.*

*Trong một phiên bản trước đây của đặc tả này, các phiên PRIMARY được gọi là các phiên MASTER. Trong cả `i2pd` và `I2P+`, chúng vẫn chỉ được biết đến với tên gọi phiên MASTER.*

SAM v3.3 bổ sung hỗ trợ chạy các phiên con streaming, datagram và raw trên cùng một phiên chính, cũng như hỗ trợ chạy nhiều phiên con cùng kiểu. Toàn bộ lưu lượng của các phiên con sử dụng chung một đích đến, hoặc một tập hợp các tunnel. Việc định tuyến lưu lượng ra khỏi I2P dựa trên các tùy chọn cổng và giao thức của các phiên con.

Để tạo các phiên phụ đa kênh, bạn phải tạo một phiên chính và sau đó thêm các phiên phụ vào phiên chính. Mỗi phiên phụ phải có một ID duy nhất và giao thức/nguồn cổng nghe (listen protocol and port) duy nhất. Các phiên phụ cũng có thể được gỡ bỏ khỏi phiên chính.

Với một phiên PRIMARY và sự kết hợp các phiên phụ (subsessions), một máy khách SAM có thể hỗ trợ nhiều ứng dụng, hoặc một ứng dụng phức tạp đơn lẻ sử dụng nhiều giao thức khác nhau, trên cùng một tập hợp các tunnel. Ví dụ, một máy khách bittorrent có thể thiết lập một phiên phụ streaming cho các kết nối ngang hàng (peer-to-peer), cùng với các phiên phụ datagram và raw cho giao tiếp DHT.

#### Tạo một phiên CHÍNH

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Cầu nối SAM sẽ phản hồi thành công hoặc thất bại như trong [phản hồi của một lệnh SESSION CREATE tiêu chuẩn](#session-creation-response).

Không đặt các tùy chọn PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL hoặc HEADER trên một phiên chính. Bạn không được gửi bất kỳ dữ liệu nào trên ID phiên chính hoặc trên socket điều khiển. Tất cả các lệnh như STREAM CONNECT, DATAGRAM SEND, v.v. phải sử dụng ID phiên phụ trên một socket riêng biệt.

Phiên CHÍNH kết nối tới bộ định tuyến và xây dựng các đường hầm. Khi cầu nối SAM phản hồi, các đường hầm đã được tạo và phiên đã sẵn sàng để thêm các phiên phụ. Tất cả các tùy chọn [I2CP](/docs/protocol/i2cp) liên quan đến các tham số đường hầm như độ dài, số lượng và biệt danh phải được cung cấp trong lệnh SESSION CREATE của phiên chính.

Tất cả các lệnh tiện ích đều được hỗ trợ trên một phiên chính.

Khi phiên chính bị đóng, tất cả các phiên phụ cũng sẽ bị đóng theo.

LƯU Ý: Trước phiên bản 0.9.47, hãy sử dụng STYLE=MASTER. STYLE=PRIMARY được hỗ trợ kể từ phiên bản 0.9.47. MASTER vẫn được hỗ trợ để đảm bảo tương thích ngược.

#### Tạo một phiên con

Sử dụng cùng một ổ cắm điều khiển mà trên đó phiên CHÍNH được tạo:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Cầu nối SAM sẽ phản hồi thành công hoặc thất bại như trong [phản hồi của một SESSION CREATE tiêu chuẩn](#session-creation-response). Vì các tunnel đã được tạo trước đó trong SESSION CREATE chính, cầu nối SAM nên phản hồi ngay lập tức.

Không đặt tùy chọn DESTINATION khi thực hiện SESSION ADD. Phiên con sẽ sử dụng đích đến được chỉ định trong phiên chính. Tất cả các phiên con đều phải được thêm vào thông qua ổ cắm điều khiển, tức là cùng kết nối mà bạn đã tạo phiên chính.

Các phiên phụ khác nhau phải có các tùy chọn đủ khác biệt để dữ liệu đầu vào có thể được định tuyến chính xác. Đặc biệt, các phiên cùng kiểu phải có các tùy chọn LISTEN_PORT khác nhau (và/hoặc LISTEN_PROTOCOL, chỉ với RAW). Việc thêm SESSION với cổng nghe và giao thức trùng với một phiên phụ hiện có sẽ dẫn đến lỗi.

LISTEN_PORT là cổng I2P cục bộ, tức là cổng nhận (TO) cho dữ liệu đến. Nếu không chỉ định LISTEN_PORT, giá trị FROM_PORT sẽ được sử dụng. Nếu cả LISTEN_PORT và FROM_PORT đều không được chỉ định, việc định tuyến dữ liệu đến sẽ dựa hoàn toàn vào STYLE và PROTOCOL. Với LISTEN_PORT và LISTEN_PROTOCOL, giá trị 0 có nghĩa là bất kỳ giá trị nào, tức là ký tự đại diện (wildcard). Nếu cả LISTEN_PORT và LISTEN_PROTOCOL đều bằng 0, phiên con này sẽ trở thành mặc định cho lưu lượng đến mà không được định tuyến tới một phiên con khác. Lưu lượng truyền tải dạng streaming (giao thức 6) sẽ không bao giờ được định tuyến đến một phiên con RAW, ngay cả khi LISTEN_PROTOCOL của nó là 0. Một phiên con RAW không được phép đặt LISTEN_PROTOCOL là 6. Nếu không có phiên con mặc định hoặc phiên con nào phù hợp với giao thức và cổng của lưu lượng đến, dữ liệu đó sẽ bị loại bỏ.

Sử dụng ID phiên phụ (subsession ID), chứ không phải ID phiên chính, để gửi và nhận dữ liệu. Tất cả các lệnh như STREAM CONNECT, DATAGRAM SEND, v.v. đều phải sử dụng ID phiên phụ.

Tất cả các lệnh tiện ích đều được hỗ trợ trên phiên chính hoặc phiên phụ. Việc gửi/nhận datagram/raw v1/v2 không được hỗ trợ trên phiên chính hoặc các phiên phụ.

#### Dừng một phiên con

Sử dụng cùng một ổ cắm điều khiển mà trên đó phiên CHÍNH được tạo:

```
->  SESSION REMOVE
          ID=$nickname
```
Thao tác này sẽ gỡ bỏ một phiên phụ khỏi phiên chính. Không đặt bất kỳ tùy chọn nào khác trên lệnh SESSION REMOVE. Các phiên phụ phải được gỡ bỏ thông qua cổng điều khiển, tức là cùng kết nối mà bạn đã tạo phiên chính. Sau khi một phiên phụ bị gỡ bỏ, nó sẽ bị đóng và không thể sử dụng để gửi hoặc nhận dữ liệu nữa.

Cầu nối SAM sẽ phản hồi thành công hoặc thất bại như trong [phản hồi của một lệnh SESSION CREATE tiêu chuẩn](#session-creation-response).

### Các lệnh tiện ích SAM

Một số lệnh tiện ích yêu cầu phiên làm việc đã tồn tại trước, trong khi một số khác thì không. Xem chi tiết bên dưới.

#### Tìm kiếm tên máy chủ

Tin nhắn sau có thể được sử dụng bởi máy khách để truy vấn cầu nối SAM nhằm phân giải tên:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
được trả lời bởi

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
Giá trị RESULT có thể là một trong các giá trị sau:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Nếu NAME=ME, phản hồi sẽ chứa đích được sử dụng bởi phiên hiện tại (hữu ích nếu bạn đang dùng phiên TRANSIENT). Nếu $result không phải là OK, MESSAGE có thể truyền tải thông điệp mô tả, ví dụ như "bad format", v.v. INVALID_KEY ngụ ý rằng có vấn đề với $name trong yêu cầu, có thể do ký tự không hợp lệ.

$destination là dạng base 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự base 64 hoặc nhiều hơn (387 byte hoặc nhiều hơn ở dạng nhị phân), tùy thuộc vào loại chữ ký.

NAMING LOOKUP không yêu cầu phải tạo phiên trước. Tuy nhiên, trong một số triển khai, việc tra cứu .b32.i2p không có trong bộ nhớ đệm và cần truy vấn mạng có thể thất bại, do không có sẵn các tunnel khách hàng để thực hiện tra cứu.

#### Tùy chọn tra cứu tên

NAMING LOOKUP đã được mở rộng kể từ phiên bản router API 0.9.66 để hỗ trợ tìm kiếm dịch vụ. Khả năng hỗ trợ có thể khác nhau tùy theo triển khai. Xem đề xuất 167 để biết thêm thông tin.

NAMING LOOKUP NAME=example.i2p OPTIONS=true yêu cầu bản ánh xạ tùy chọn trong phản hồi. NAME có thể là đích base64 đầy đủ khi OPTIONS=true.

Nếu việc tra cứu đích thành công và có các tùy chọn trong leaseset, thì trong phản hồi, sau phần đích, sẽ có một hoặc nhiều tùy chọn dưới dạng OPTION:key=value. Mỗi tùy chọn sẽ có tiền tố OPTION: riêng. Tất cả các tùy chọn từ leaseset sẽ được bao gồm, không chỉ những tùy chọn bản ghi dịch vụ. Ví dụ, các tùy chọn cho các tham số được định nghĩa trong tương lai cũng có thể xuất hiện. Ví dụ:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Các khóa chứa dấu '=', và các khóa hoặc giá trị chứa ký tự xuống dòng, sẽ bị coi là không hợp lệ và cặp khóa/giá trị đó sẽ bị loại bỏ khỏi phản hồi. Nếu không tìm thấy tùy chọn nào trong leaseset, hoặc nếu leaseset là phiên bản 1, thì phản hồi sẽ không bao gồm bất kỳ tùy chọn nào. Nếu OPTIONS=true được đặt trong truy vấn tra cứu và leaseset không được tìm thấy, một giá trị kết quả mới LEASESET_NOT_FOUND sẽ được trả về.

#### Tạo khóa đích

Các khóa base64 công khai và riêng tư có thể được tạo bằng tin nhắn sau:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
được trả lời bởi

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Kể từ phiên bản 3.1 (I2P 0.9.14), một tham số tùy chọn SIGNATURE_TYPE được hỗ trợ. Giá trị SIGNATURE_TYPE có thể là bất kỳ tên nào (ví dụ: ECDSA_SHA256_P256, không phân biệt chữ hoa/thường) hoặc số (ví dụ: 1) mà [Chứng chỉ khóa](/docs/specs/common-structures#type_Certificate) hỗ trợ. Giá trị mặc định là DSA_SHA1, ĐÂY KHÔNG PHẢI là thứ bạn muốn. Đối với hầu hết các ứng dụng, vui lòng chỉ định SIGNATURE_TYPE=7.

$destination là dạng base 64 của [Destination](/docs/specs/common-structures#type_Destination), gồm 516 ký tự base 64 hoặc nhiều hơn (387 byte hoặc nhiều hơn ở dạng nhị phân), tùy thuộc vào loại chữ ký.

$privkey là dạng base 64 của chuỗi nối giữa [Destination](/docs/specs/common-structures#type_Destination), tiếp theo là [Private Key](/docs/specs/common-structures#type_PrivateKey), rồi đến [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), có độ dài ít nhất 884 ký tự base 64 (tương ứng 663 byte hoặc nhiều hơn trong dạng nhị phân), tùy thuộc vào loại chữ ký. Định dạng nhị phân được mô tả trong tài liệu Private Key File.

Ghi chú về khóa riêng nhị phân 256 byte [Private Key](/docs/specs/common-structures#type_PrivateKey): Trường này đã không được sử dụng kể từ phiên bản 0.6 (2005). Các triển khai SAM có thể gửi dữ liệu ngẫu nhiên hoặc toàn bộ số 0 vào trường này; đừng lo lắng nếu thấy chuỗi AAAA trong mã hóa base 64. Hầu hết các ứng dụng sẽ đơn giản lưu trữ chuỗi base 64 và trả lại nguyên dạng trong SESSION CREATE, hoặc giải mã sang nhị phân để lưu trữ, sau đó mã hóa lại khi thực hiện SESSION CREATE. Tuy nhiên, các ứng dụng có thể giải mã base 64, phân tích dữ liệu nhị phân theo đặc tả PrivateKeyFile, loại bỏ phần khóa riêng 256 byte, rồi thay thế bằng 256 byte dữ liệu ngẫu nhiên hoặc toàn bộ số 0 khi mã hóa lại cho SESSION CREATE. TẤT CẢ các trường khác trong đặc tả PrivateKeyFile phải được giữ nguyên. Cách làm này sẽ tiết kiệm được 256 byte dung lượng lưu trữ trên hệ thống tập tin nhưng có lẽ không đáng để thực hiện trong hầu hết các ứng dụng. Xem đề xuất 161 để biết thêm thông tin và bối cảnh liên quan.

DEST GENERATE không yêu cầu phải tạo phiên trước tiên.

DEST GENERATE không thể được dùng để tạo một đích đến với chữ ký ngoại tuyến.

#### PING/PONG (SAM 3.2 hoặc cao hơn)

Máy khách hoặc máy chủ đều có thể gửi:

```
PING[ arbitrary text]
```
trên cổng điều khiển, với phản hồi:

```
PONG[ arbitrary text from the ping]
```
được sử dụng để giữ kết nối socket điều khiển hoạt động. Một trong hai phía có thể đóng phiên và socket nếu không nhận được phản hồi trong một khoảng thời gian hợp lý, tùy thuộc vào cách triển khai.

Nếu xảy ra hết thời gian chờ khi đợi PONG từ máy khách, cầu nối có thể gửi:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
và sau đó ngắt kết nối.

Nếu thời gian chờ kết thúc khi đang đợi PONG từ cầu nối, máy khách có thể đơn giản ngắt kết nối.

PING/PONG không yêu cầu phải tạo phiên trước tiên.

#### QUIT/STOP/EXIT (SAM 3.2 hoặc cao hơn, các tính năng tùy chọn)

Các lệnh QUIT, STOP và EXIT sẽ đóng phiên làm việc và socket. Việc triển khai là tùy chọn, nhằm thuận tiện cho việc kiểm thử thông qua telnet. Việc có phản hồi nào trước khi socket bị đóng (ví dụ: thông báo SESSION STATUS) hay không phụ thuộc vào cách triển khai và nằm ngoài phạm vi của đặc tả này.

QUIT/STOP/EXIT không yêu cầu phiên phải được tạo trước.

#### TRỢ GIÚP (tính năng tùy chọn)

Các máy chủ có thể triển khai lệnh HELP. Việc triển khai là tùy chọn, nhằm thuận tiện cho việc kiểm thử thông qua telnet. Định dạng đầu ra và việc xác định điểm kết thúc của đầu ra phụ thuộc vào từng cách triển khai và nằm ngoài phạm vi của đặc tả này.

HELP không yêu cầu phải tạo phiên trước tiên.

#### Cấu hình ủy quyền (SAM 3.2 hoặc cao hơn, tính năng tùy chọn)

Cấu hình ủy quyền sử dụng lệnh AUTH. Máy chủ SAM có thể triển khai các lệnh này để hỗ trợ lưu trữ thông tin đăng nhập một cách bền vững. Việc cấu hình xác thực bằng các phương pháp khác ngoài các lệnh này phụ thuộc vào từng phần triển khai cụ thể và nằm ngoài phạm vi của đặc tả này.

- AUTH ENABLE bật xác thực cho các kết nối tiếp theo
- AUTH DISABLE tắt xác thực cho các kết nối tiếp theo
- AUTH ADD USER="foo" PASSWORD="bar" thêm người dùng/mật khẩu
- AUTH REMOVE USER="foo" xóa người dùng này

Nên dùng dấu ngoặc kép cho tên người dùng và mật khẩu nhưng không bắt buộc. Một dấu ngoặc kép bên trong tên người dùng hoặc mật khẩu phải được thoát bằng dấu gạch ngược. Nếu thất bại, máy chủ sẽ phản hồi bằng I2P_ERROR và một thông điệp.

AUTH không yêu cầu phiên phải được tạo trước tiên.

### Các giá trị RESULT

Đây là các giá trị có thể được mang bởi trường RESULT, cùng với ý nghĩa của chúng:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Các triển khai khác nhau có thể không nhất quán về việc trả về RESULT nào trong các tình huống khác nhau.

Hầu hết các phản hồi có RESULT khác ngoài OK cũng sẽ bao gồm một MESSAGE chứa thông tin bổ sung. Nội dung MESSAGE thường hữu ích để gỡ lỗi các sự cố. Tuy nhiên, các chuỗi MESSAGE phụ thuộc vào cách triển khai cụ thể, có thể được hoặc không được máy chủ SAM dịch sang ngôn ngữ hiện tại, có thể chứa thông tin nội bộ đặc thù triển khai như các ngoại lệ, và có thể thay đổi mà không cần thông báo trước. Mặc dù các ứng dụng khách SAM có thể lựa chọn hiển thị các chuỗi MESSAGE cho người dùng, họ không nên đưa ra các quyết định trong chương trình dựa trên những chuỗi này, vì điều đó sẽ khiến hệ thống trở nên kém ổn định.

### Tùy chọn Tunnels, I2CP và Streaming

Các tùy chọn này có thể được truyền vào dưới dạng các cặp tên=giá trị trong dòng SAM SESSION CREATE.

Tất cả các phiên có thể bao gồm [các tùy chọn I2CP như độ dài và số lượng tunnel](/docs/protocol/i2cp#options). Các phiên STREAM có thể bao gồm [các tùy chọn của thư viện Streaming](/docs/api/streaming#options).

Xem các tài liệu tham khảo đó để biết tên tùy chọn và giá trị mặc định. Tài liệu được tham chiếu ở đây dành cho triển khai router bằng Java. Các giá trị mặc định có thể thay đổi theo thời gian. Tên và giá trị tùy chọn phân biệt chữ hoa chữ thường. Các triển khai router khác có thể không hỗ trợ tất cả các tùy chọn và có thể có giá trị mặc định khác nhau; vui lòng tham khảo tài liệu của router cụ thể để biết chi tiết.

### Ghi chú BASE 64

Việc mã hóa Base 64 phải sử dụng bảng chữ cái Base 64 chuẩn I2P là "A-Z, a-z, 0-9, -, ~".

### Thiết lập SAM mặc định

Cổng SAM mặc định là 7656. SAM không được bật theo mặc định trong Java I2P Router; bạn phải khởi động thủ công, hoặc cấu hình để tự động khởi động, thông qua trang cấu hình clients trong bảng điều khiển router, hoặc trong tập tin clients.config. Cổng UDP SAM mặc định là 7655, lắng nghe trên 127.0.0.1. Các cổng này có thể được thay đổi trong Java router bằng cách thêm các tham số sam.udp.port=nnnnn và/hoặc sam.udp.host=w.x.y.z vào lệnh khởi chạy, hoặc trên dòng SESSION.

Cấu hình trong các router khác phụ thuộc vào cách triển khai cụ thể. Xem [hướng dẫn cấu hình i2pd tại đây](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
