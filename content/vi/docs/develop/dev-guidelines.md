---
title: "Hướng dẫn Phát triển và Phong cách Lập trình"
description: "Hướng dẫn toàn diện về đóng góp cho I2P: quy trình làm việc, chu kỳ phát hành, phong cách lập trình, ghi log, cấp phép và xử lý vấn đề"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Đọc [Hướng dẫn cho Nhà phát triển mới](/docs/develop/new-developers/) trước.

## Hướng dẫn Cơ bản và Phong cách Lập trình

Hầu hết những điều sau đây là thường thức đối với bất kỳ ai đã làm việc với mã nguồn mở hoặc trong môi trường lập trình thương mại. Những điều sau đây áp dụng chủ yếu cho nhánh phát triển chính i2p.i2p. Các hướng dẫn cho các nhánh khác, plugin và ứng dụng bên ngoài có thể khác biệt đáng kể; hãy liên hệ với nhà phát triển phù hợp để được hướng dẫn.

### Cộng đồng

- Vui lòng đừng chỉ viết code. Nếu có thể, hãy tham gia vào các hoạt động phát triển khác, bao gồm: thảo luận phát triển và hỗ trợ trên IRC và i2pforum.i2p; kiểm thử; báo cáo lỗi và phản hồi; tài liệu; đánh giá code; v.v.
- Các lập trình viên tích cực nên có mặt định kỳ trên IRC `#i2p-dev`. Luôn nắm rõ chu kỳ phát hành hiện tại. Tuân thủ các mốc phát hành như đóng băng tính năng, đóng băng thẻ, và thời hạn check-in cho bản phát hành.

### Chu kỳ phát hành

Chu kỳ phát hành thông thường là 10–16 tuần, bốn lần phát hành mỗi năm. Sau đây là các thời hạn gần đúng trong một chu kỳ 13 tuần điển hình. Thời hạn thực tế cho mỗi bản phát hành được người quản lý phát hành thiết lập sau khi tham khảo ý kiến toàn bộ nhóm.

- 1–2 ngày sau bản phát hành trước: Được phép check-in vào trunk.
- 2–3 tuần sau bản phát hành trước: Hạn chót để lan truyền các thay đổi lớn từ các nhánh khác sang trunk.
- 4–5 tuần trước khi phát hành: Hạn chót để yêu cầu các liên kết trang chủ mới.
- 3–4 tuần trước khi phát hành: Đóng băng tính năng. Hạn chót cho các tính năng mới lớn.
- 2–3 tuần trước khi phát hành: Tổ chức cuộc họp dự án để xem xét các yêu cầu liên kết trang chủ mới, nếu có.
- 10–14 ngày trước khi phát hành: Đóng băng chuỗi dịch. Không thay đổi thêm các chuỗi đã dịch (đã gắn thẻ). Đẩy các chuỗi lên Transifex, thông báo hạn chót dịch thuật trên Transifex.
- 10–14 ngày trước khi phát hành: Hạn chót tính năng. Chỉ sửa lỗi sau thời điểm này. Không thêm tính năng, tái cấu trúc hoặc dọn dẹp mã.
- 3–4 ngày trước khi phát hành: Hạn chót dịch thuật. Kéo các bản dịch từ Transifex và check-in.
- 3–4 ngày trước khi phát hành: Hạn chót check-in. Không check-in sau thời điểm này nếu không có sự cho phép của người xây dựng bản phát hành.
- Vài giờ trước khi phát hành: Hạn chót đánh giá mã.

### Git

- Có hiểu biết cơ bản về hệ thống quản lý mã nguồn phân tán, ngay cả khi bạn chưa từng sử dụng git trước đây. Hãy yêu cầu trợ giúp nếu cần. Một khi đã push, các check-in sẽ tồn tại mãi mãi; không có cách nào hoàn tác. Vui lòng thận trọng. Nếu bạn chưa từng sử dụng git, hãy bắt đầu từng bước nhỏ. Check in một số thay đổi nhỏ và xem kết quả như thế nào.
- Kiểm tra các thay đổi của bạn trước khi check in. Nếu bạn thích mô hình phát triển check-in-trước-test, hãy sử dụng nhánh phát triển riêng trong tài khoản của bạn và tạo MR khi công việc hoàn tất. Không làm hỏng bản build. Không gây ra regression (lỗi thoái lui). Trong trường hợp bạn gây ra (điều này xảy ra), vui lòng không biến mất trong thời gian dài sau khi push thay đổi của bạn.
- Nếu thay đổi của bạn không đơn giản, hoặc bạn muốn mọi người kiểm tra nó và cần báo cáo kiểm tra tốt để biết liệu thay đổi của bạn đã được kiểm tra hay chưa, hãy thêm nhận xét check-in vào `history.txt` và tăng phiên bản build trong `RouterVersion.java`.
- Không check in các thay đổi lớn vào nhánh chính i2p.i2p muộn trong chu kỳ phát hành. Nếu một dự án sẽ mất hơn vài ngày, hãy tạo nhánh riêng trong git, trong tài khoản của bạn, và thực hiện phát triển ở đó để không chặn các bản phát hành.
- Đối với các thay đổi lớn (nói chung, hơn 100 dòng hoặc ảnh hưởng đến hơn ba tệp), hãy check in vào một nhánh mới trên tài khoản GitLab của bạn, tạo MR và chỉ định người đánh giá. Gán MR cho chính bạn. Tự merge MR sau khi người đánh giá phê duyệt.
- Không tạo nhánh WIP trong tài khoản I2P_Developers chính (trừ i2p.www). WIP thuộc về tài khoản riêng của bạn. Khi công việc hoàn tất, hãy tạo MR. Các nhánh duy nhất trong tài khoản chính chỉ nên dành cho các fork thực sự, như bản phát hành điểm.
- Thực hiện phát triển một cách minh bạch và hướng đến cộng đồng. Check in thường xuyên. Check in hoặc merge vào nhánh chính càng thường xuyên càng tốt, theo các hướng dẫn trên. Nếu bạn đang làm việc trên một dự án lớn trong nhánh/tài khoản riêng của mình, hãy cho mọi người biết để họ có thể theo dõi và xem xét/kiểm tra/nhận xét.

### Phong Cách Lập Trình

- Phong cách code trong hầu hết mã nguồn là 4 dấu cách để thụt lề. Không sử dụng tab. Không định dạng lại code. Nếu IDE hoặc editor của bạn muốn định dạng lại mọi thứ, hãy kiểm soát nó. Ở một số nơi, phong cách code có thể khác. Hãy sử dụng lẽ thường. Mô phỏng phong cách trong file bạn đang chỉnh sửa.
- Tất cả các class và method public và package-private mới đều yêu cầu Javadocs. Thêm `@since` release-number. Javadocs cho các method private mới là điều mong muốn.
- Đối với bất kỳ Javadocs nào được thêm vào, không được có bất kỳ lỗi hoặc cảnh báo doclint nào. Chạy `ant javadoc` với Oracle Java 14 hoặc cao hơn để kiểm tra. Tất cả params phải có dòng `@param`, tất cả method không phải void phải có dòng `@return`, tất cả exception được khai báo throw phải có dòng `@throws`, và không có lỗi HTML.
- Các class trong `core/` (i2p.jar) và một phần của i2ptunnel là một phần của API chính thức của chúng tôi. Có một số plugin ngoài cây mã nguồn và các ứng dụng khác phụ thuộc vào API này. Hãy cẩn thận không thực hiện bất kỳ thay đổi nào phá vỡ tính tương thích. Đừng thêm method vào API trừ khi chúng có tính tiện ích chung. Javadocs cho các method API nên rõ ràng và đầy đủ. Nếu bạn thêm hoặc thay đổi API, cũng cập nhật tài liệu trên website (nhánh i2p.www).
- Đánh dấu các chuỗi để dịch khi thích hợp, điều này đúng với tất cả chuỗi UI. Đừng thay đổi các chuỗi đã được đánh dấu trừ khi thực sự cần thiết, vì nó sẽ phá vỡ các bản dịch hiện có. Không thêm hoặc thay đổi các chuỗi đã đánh dấu sau khi đóng băng tag trong chu kỳ phát hành để người dịch có cơ hội cập nhật trước khi phát hành.
- Sử dụng generics và các class concurrent khi có thể. I2P là một ứng dụng đa luồng cao.
- Làm quen với các lỗi Java phổ biến được phát hiện bởi FindBugs/SpotBugs. Chạy `ant findbugs` để tìm hiểu thêm.
- Java 8 là yêu cầu để build và chạy I2P từ phiên bản 0.9.47. Không sử dụng các class hoặc method của Java 7 hoặc 8 trong các hệ thống con nhúng: addressbook, core, i2ptunnel.jar (non‑UI), mstreaming, router, routerconsole (chỉ news), streaming. Các hệ thống con này được sử dụng bởi Android và các ứng dụng nhúng chỉ yêu cầu Java 6. Tất cả các class phải có sẵn trong Android API 14. Các tính năng ngôn ngữ Java 7 có thể chấp nhận được trong các hệ thống con này nếu được hỗ trợ bởi phiên bản hiện tại của Android SDK và chúng biên dịch thành code tương thích Java 6.
- Try‑with‑resources không thể được sử dụng trong các hệ thống con nhúng vì nó yêu cầu `java.lang.AutoCloseable` trong runtime, và điều này không có sẵn cho đến Android API 19 (KitKat 4.4).
- Package `java.nio.file` không thể được sử dụng trong các hệ thống con nhúng vì nó không có sẵn cho đến Android API 26 (Oreo 8).
- Ngoài các hạn chế trên, các class, method và cấu trúc Java 8 chỉ có thể được sử dụng trong các hệ thống con sau: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (trừ news), SAM, susidns, susimail, systray.
- Tác giả plugin có thể yêu cầu bất kỳ phiên bản Java tối thiểu nào thông qua file `plugin.config`.
- Chuyển đổi rõ ràng giữa các kiểu nguyên thủy và class; đừng dựa vào autoboxing/unboxing.
- Đừng sử dụng `URL`. Hãy sử dụng `URI`.
- Đừng catch `Exception`. Hãy catch `RuntimeException` và các checked exception riêng lẻ.
- Đừng sử dụng `String.getBytes()` mà không có tham số charset UTF‑8. Bạn cũng có thể sử dụng `DataHelper.getUTF8()` hoặc `DataHelper.getASCII()`.
- Luôn chỉ định charset UTF‑8 khi đọc hoặc ghi file. Các tiện ích `DataHelper` có thể hữu ích.
- Luôn chỉ định một locale (ví dụ `Locale.US`) khi sử dụng `String.toLowerCase()` hoặc `String.toUpperCase()`. Không sử dụng `String.equalsIgnoreCase()`, vì không thể chỉ định locale.
- Đừng sử dụng `String.split()`. Hãy sử dụng `DataHelper.split()`.
- Đừng thêm code để định dạng ngày và giờ. Hãy sử dụng `DataHelper.formatDate()` và `DataHelper.formatTime()`.
- Đảm bảo rằng `InputStream` và `OutputStream` được đóng trong các khối finally.
- Sử dụng `{}` cho tất cả các khối `for` và `while`, ngay cả khi chỉ có một dòng. Nếu bạn sử dụng `{}` cho khối `if`, `else` hoặc `if-else`, hãy sử dụng nó cho tất cả các khối. Đặt `} else {` trên một dòng duy nhất.
- Chỉ định các field là `final` bất cứ khi nào có thể.
- Đừng lưu trữ `I2PAppContext`, `RouterContext`, `Log`, hoặc bất kỳ tham chiếu nào khác đến router hoặc các mục context trong các field static.
- Đừng khởi động thread trong constructor. Sử dụng `I2PAppThread` thay vì `Thread`.

### Ghi nhật ký

Các hướng dẫn sau đây áp dụng cho router, ứng dụng web và tất cả các plugin.

- Đối với bất kỳ thông báo nào không được hiển thị ở mức log mặc định (WARN, INFO, và DEBUG), trừ khi thông báo là một chuỗi tĩnh (không nối chuỗi), luôn sử dụng `log.shouldWarn()`, `log.shouldInfo()`, hoặc `log.shouldDebug()` trước lệnh gọi log để tránh tạo ra các đối tượng không cần thiết.
- Thông báo log có thể được hiển thị ở mức log mặc định (ERROR, CRIT, và `logAlways()`) nên ngắn gọn, rõ ràng và dễ hiểu đối với người dùng không có chuyên môn kỹ thuật. Điều này bao gồm văn bản lý do exception có thể cũng được hiển thị. Cân nhắc dịch nếu lỗi có khả năng xảy ra (ví dụ: lỗi khi gửi biểu mẫu). Nếu không, việc dịch không bắt buộc, nhưng có thể hữu ích khi tìm kiếm và tái sử dụng chuỗi đã được gắn thẻ để dịch ở nơi khác.
- Thông báo log không được hiển thị ở mức log mặc định (WARN, INFO, và DEBUG) được dành cho nhà phát triển sử dụng, và không cần đáp ứng các yêu cầu trên. Tuy nhiên, thông báo WARN có sẵn trong tab log của Android, và có thể hỗ trợ người dùng khi gỡ lỗi vấn đề, vì vậy cũng cần cẩn thận với thông báo WARN.
- Thông báo log INFO và DEBUG nên được sử dụng một cách tiết kiệm, đặc biệt trong các đoạn code thực thi thường xuyên. Mặc dù hữu ích trong quá trình phát triển, hãy cân nhắc xóa chúng hoặc chuyển thành comment sau khi hoàn thành kiểm thử.
- Không log ra stdout hoặc stderr (wrapper log).

### Giấy phép

- Chỉ check in code mà bạn tự viết. Trước khi check in bất kỳ code hoặc file JAR thư viện nào từ nguồn khác, hãy giải trình lý do cần thiết, xác minh giấy phép tương thích, và xin phê duyệt từ release manager (người quản lý phát hành).
- Nếu bạn được phê duyệt để thêm code hoặc file JAR bên ngoài, và các file nhị phân có sẵn trong bất kỳ gói Debian hoặc Ubuntu nào, bạn phải triển khai các tùy chọn build và packaging để sử dụng gói bên ngoài thay thế. Danh sách các file cần sửa đổi: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Đối với bất kỳ hình ảnh nào được check in từ nguồn bên ngoài, bạn có trách nhiệm xác minh trước giấy phép có tương thích hay không. Bao gồm thông tin giấy phép và nguồn trong comment khi check in.

### Lỗi

- Quản lý các vấn đề là công việc của tất cả mọi người; vui lòng giúp đỡ. Theo dõi [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) để tìm các vấn đề mà bạn có thể hỗ trợ. Bình luận, sửa chữa và đóng các vấn đề nếu bạn có thể.
- Các nhà phát triển mới nên bắt đầu bằng việc sửa các vấn đề. Khi bạn có bản sửa lỗi, đính kèm bản vá của bạn vào vấn đề và thêm từ khóa `review-needed`. Không đóng vấn đề cho đến khi nó đã được xem xét thành công và bạn đã kiểm tra các thay đổi của mình. Sau khi bạn đã thực hiện điều này suôn sẻ cho một vài ticket, bạn có thể tuân theo quy trình thông thường ở trên.
- Đóng một vấn đề khi bạn nghĩ rằng bạn đã sửa nó. Chúng tôi không có bộ phận kiểm thử để xác minh và đóng các ticket. Nếu bạn không chắc chắn rằng mình đã sửa nó, hãy đóng nó và thêm ghi chú "Tôi nghĩ rằng tôi đã sửa nó, vui lòng kiểm tra và mở lại nếu nó vẫn bị lỗi". Thêm bình luận với số phiên bản dev build hoặc revision và đặt milestone cho bản phát hành tiếp theo.
