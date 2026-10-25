---
title: "Mô hình Mối đe dọa của I2P"
description: "Phân tích các cuộc tấn công được xem xét trong thiết kế của I2P và các biện pháp giảm thiểu đã được triển khai"
slug: "threat-model"
aliases:
  - "/vi/how_threatmodel"
  - "/vi/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## Chúng ta hiểu gì khi nói "Ẩn danh"?

Mức độ ẩn danh của bạn có thể được mô tả là "mức độ khó khăn để ai đó tìm ra thông tin mà bạn không muốn họ biết" — bạn là ai, bạn ở đâu, bạn giao tiếp với ai, hoặc thậm chí khi nào bạn giao tiếp. Khái niệm ẩn danh "hoàn hảo" không hữu ích ở đây — phần mềm sẽ không thể làm cho bạn không thể phân biệt được với những người không sử dụng máy tính hoặc không có trên Internet. Thay vào đó, chúng tôi đang nỗ lực cung cấp mức độ ẩn danh đủ để đáp ứng nhu cầu thực tế của bất kỳ ai có thể — từ những người đơn giản chỉ duyệt web, đến những người trao đổi dữ liệu, đến những người sợ bị phát hiện bởi các tổ chức hoặc nhà nước có quyền lực.

Câu hỏi về việc liệu I2P có cung cấp đủ tính ẩn danh cho nhu cầu cụ thể của bạn hay không là một câu hỏi khó, nhưng trang này hy vọng sẽ hỗ trợ trả lời câu hỏi đó bằng cách khám phá cách I2P hoạt động dưới các cuộc tấn công khác nhau để bạn có thể quyết định xem nó có đáp ứng nhu cầu của bạn hay không.

Chúng tôi hoan nghênh các nghiên cứu và phân tích sâu hơn về khả năng chống chọi của I2P trước các mối đe dọa được mô tả dưới đây. Cần có thêm việc rà soát tài liệu hiện có (phần lớn tập trung vào Tor) và các nghiên cứu gốc tập trung vào I2P.

---

## Tóm tắt Cấu trúc Mạng

I2P được xây dựng dựa trên các ý tưởng của nhiều [hệ thống khác](/docs/overview/comparison/), nhưng cần lưu ý một số điểm quan trọng khi xem xét tài liệu liên quan:

- **I2P là một mixnet tuyến đường miễn phí** — người tạo thông điệp định nghĩa rõ ràng đường đi mà thông điệp sẽ được gửi đi (outbound tunnel), và người nhận thông điệp định nghĩa rõ ràng đường đi mà thông điệp sẽ được nhận trên đó (inbound tunnel).
- **I2P không có điểm vào và ra chính thức** — tất cả các peer tham gia đầy đủ vào quá trình trộn, và không có proxy vào hoặc ra ở tầng mạng (tuy nhiên, ở tầng ứng dụng, một số proxy tồn tại).
- **I2P được phân phối hoàn toàn** — không có kiểm soát trung tâm hay cơ quan quyền lực. Người ta có thể chỉnh sửa một số router để vận hành các mix cascade (xây dựng tunnel và cung cấp các khóa cần thiết để kiểm soát việc chuyển tiếp tại điểm cuối tunnel) hoặc lập hồ sơ và lựa chọn dựa trên thư mục, tất cả đều không phá vỡ tính tương thích với phần còn lại của mạng, nhưng làm như vậy tất nhiên là không cần thiết (và thậm chí có thể gây hại cho tính ẩn danh của bạn).

Chúng tôi đã lập kế hoạch chi tiết để triển khai các chiến lược độ trễ và xử lý theo lô không tầm thường, mà sự tồn tại của chúng chỉ được biết bởi hop cụ thể hoặc tunnel gateway nhận thông điệp, cho phép một mixnet chủ yếu có độ trễ thấp cung cấp lưu lượng che giấu cho giao tiếp có độ trễ cao hơn (ví dụ: email). Tuy nhiên, chúng tôi nhận thức rằng cần có độ trễ đáng kể để cung cấp sự bảo vệ có ý nghĩa, và việc triển khai những độ trễ như vậy sẽ là một thách thức lớn. Tại thời điểm này, chưa rõ liệu chúng tôi có thực sự triển khai các tính năng độ trễ này hay không.

Về mặt lý thuyết, các router dọc theo đường đi của thông điệp có thể chèn thêm một số lượng bất kỳ các hop trước khi chuyển tiếp thông điệp đến peer tiếp theo, mặc dù việc triển khai hiện tại không làm như vậy.

---

## Mô hình Mối đe dọa

Thiết kế I2P bắt đầu vào năm 2003, không lâu sau khi [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/), và [Tor](https://www.torproject.org/) ra đời. Thiết kế của chúng tôi được hưởng lợi đáng kể từ các nghiên cứu được công bố vào thời gian đó. I2P sử dụng một số kỹ thuật onion routing (định tuyến hành tây), vì vậy chúng tôi tiếp tục được hưởng lợi từ sự quan tâm học thuật đáng kể dành cho Tor.

Dựa trên các cuộc tấn công và phân tích được trình bày trong [tài liệu về tính ẩn danh](http://freehaven.net/anonbib/topic.html) (chủ yếu là [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)), phần sau đây mô tả ngắn gọn nhiều loại tấn công đa dạng cũng như nhiều biện pháp phòng thủ của I2P. Chúng tôi cập nhật danh sách này để bao gồm các cuộc tấn công mới khi chúng được xác định.

Bao gồm một số cuộc tấn công có thể độc nhất đối với I2P. Chúng tôi không có câu trả lời tốt cho tất cả các cuộc tấn công này, tuy nhiên chúng tôi tiếp tục nghiên cứu và cải thiện hệ thống phòng thủ.

Ngoài ra, nhiều cuộc tấn công này dễ dàng hơn đáng kể so với mức độ khó khăn mà chúng nên có, do quy mô khiêm tốn của mạng lưới hiện tại. Mặc dù chúng tôi nhận thức được một số hạn chế cần được giải quyết, I2P được thiết kế để hỗ trợ hàng trăm nghìn, hoặc hàng triệu người tham gia. Khi chúng tôi tiếp tục lan truyền thông tin và mở rộng mạng lưới, các cuộc tấn công này sẽ trở nên khó khăn hơn nhiều.

Các trang [so sánh mạng](/docs/overview/comparison/) và [thuật ngữ "garlic"](/docs/overview/garlic-routing/) cũng có thể hữu ích để xem xét.

### Tấn Công Brute Force

Một cuộc tấn công brute force có thể được thực hiện bởi một kẻ thù thụ động hoặc chủ động toàn cầu, theo dõi tất cả các thông điệp truyền qua giữa tất cả các nút và cố gắng liên kết thông điệp nào đi theo đường dẫn nào. Việc thực hiện cuộc tấn công này chống lại I2P sẽ không hề đơn giản, vì tất cả các peer trong mạng thường xuyên gửi thông điệp (cả thông điệp end-to-end và bảo trì mạng), cộng với việc một thông điệp end-to-end thay đổi kích thước và dữ liệu dọc theo đường đi của nó. Thêm vào đó, kẻ thù bên ngoài cũng không có quyền truy cập vào các thông điệp, vì giao tiếp giữa các router vừa được mã hóa vừa được truyền dưới dạng luồng (làm cho hai thông điệp 1024 byte không thể phân biệt được với một thông điệp 2048 byte).

Tuy nhiên, một kẻ tấn công mạnh mẽ có thể sử dụng brute force để phát hiện xu hướng — nếu họ có thể gửi 5GB đến một đích I2P và giám sát kết nối mạng của mọi người, họ có thể loại bỏ tất cả các peer không nhận được 5GB dữ liệu. Các kỹ thuật để đánh bại cuộc tấn công này tồn tại, nhưng có thể quá tốn kém (xem: [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)'s mimics hoặc lưu lượng tốc độ không đổi). Hầu hết người dùng không quan tâm đến cuộc tấn công này, vì chi phí thực hiện nó là cực kỳ cao (và thường yêu cầu hoạt động bất hợp pháp). Tuy nhiên, cuộc tấn công vẫn có thể xảy ra, ví dụ bởi một người quan sát tại một ISP lớn hoặc điểm trao đổi Internet. Những người muốn bảo vệ chống lại nó sẽ muốn thực hiện các biện pháp đối phó thích hợp, chẳng hạn như đặt giới hạn băng thông thấp, và sử dụng leaseSet không được công bố hoặc được mã hóa cho các I2P Site. Các biện pháp đối phó khác, chẳng hạn như độ trễ không tầm thường và tuyến đường hạn chế, hiện tại chưa được triển khai.

Như một biện pháp phòng thủ một phần chống lại một router đơn lẻ hoặc nhóm router cố gắng định tuyến toàn bộ lưu lượng của mạng, các router chứa các giới hạn về số lượng tunnel có thể được định tuyến qua một peer duy nhất. Khi mạng phát triển, những giới hạn này có thể được điều chỉnh thêm. Các cơ chế khác để đánh giá, lựa chọn và tránh peer được thảo luận trong trang lựa chọn peer.

### Tấn Công Thời Gian

Các thông điệp của I2P là đơn hướng và không nhất thiết ngụ ý rằng sẽ có phản hồi được gửi. Tuy nhiên, các ứng dụng chạy trên I2P rất có thể sẽ có các mẫu nhận dạng được trong tần suất thông điệp của chúng — ví dụ, một yêu cầu HTTP sẽ là một thông điệp nhỏ với một chuỗi lớn các thông điệp phản hồi chứa phản hồi HTTP. Sử dụng dữ liệu này cũng như cái nhìn tổng quan về cấu trúc mạng, kẻ tấn công có thể loại bỏ một số liên kết vì quá chậm để có thể truyền thông điệp đó.

Loại tấn công này rất mạnh mẽ, nhưng khả năng áp dụng vào I2P không rõ ràng, vì sự biến động trong độ trễ tin nhắn do xếp hàng, xử lý tin nhắn và điều chỉnh tốc độ thường sẽ bằng hoặc vượt quá thời gian truyền tin nhắn qua một liên kết duy nhất — ngay cả khi kẻ tấn công biết rằng phản hồi sẽ được gửi ngay khi tin nhắn được nhận. Tuy nhiên, có một số tình huống sẽ để lộ các phản hồi khá tự động — thư viện streaming thực hiện điều này (với SYN+ACK) cũng như chế độ tin nhắn đảm bảo giao hàng (với DataMessage+DeliveryStatusMessage).

Nếu không có protocol scrubbing hoặc độ trễ cao hơn, các đối thủ tích cực toàn cục có thể thu thập được thông tin đáng kể. Do đó, những người lo ngại về các cuộc tấn công này có thể tăng độ trễ (sử dụng các chiến lược trì hoãn không tầm thường hoặc xử lý theo lô), bao gồm protocol scrubbing, hoặc các kỹ thuật định tuyến tunnel nâng cao khác, nhưng những điều này chưa được triển khai trong I2P.

Tài liệu tham khảo: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Tấn công giao điểm

Các cuộc tấn công giao điểm chống lại các hệ thống độ trễ thấp cực kỳ mạnh mẽ — định kỳ liên lạc với mục tiêu và theo dõi những peer nào đang trên mạng. Theo thời gian, khi xảy ra hiện tượng node churn (nút mạng thay đổi), kẻ tấn công sẽ thu được thông tin đáng kể về mục tiêu chỉ bằng cách giao điểm các tập hợp peer đang trực tuyến khi một tin nhắn được truyền đi thành công. Chi phí của cuộc tấn công này rất lớn khi mạng phát triển, nhưng có thể khả thi trong một số tình huống.

Tóm lại, nếu kẻ tấn công có mặt ở cả hai đầu tunnel của bạn cùng một lúc, họ có thể thành công. I2P không có biện pháp phòng thủ hoàn toàn chống lại điều này đối với giao tiếp độ trễ thấp. Đây là điểm yếu cố hữu của onion routing độ trễ thấp. Tor cũng cung cấp [tuyên bố từ chối trách nhiệm tương tự](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting).

Các biện pháp phòng thủ một phần được triển khai trong I2P:

- [Sắp xếp nghiêm ngặt](/docs/specs/tunnel-implementation/#ordering) các peer
- Lập hồ sơ và lựa chọn peer từ một nhóm nhỏ thay đổi chậm
- Giới hạn số lượng tunnel được định tuyến qua một peer duy nhất
- Ngăn chặn các peer từ cùng dải IP /16 trở thành thành viên của một tunnel duy nhất
- Đối với I2P Sites hoặc các dịch vụ lưu trữ khác, chúng tôi hỗ trợ lưu trữ đồng thời trên nhiều router, hoặc multihoming

Ngay cả khi kết hợp tất cả lại, những biện pháp phòng thủ này vẫn không phải là giải pháp hoàn chỉnh. Ngoài ra, chúng tôi đã đưa ra một số quyết định thiết kế có thể làm tăng đáng kể tính dễ bị tấn công của chúng tôi:

- Chúng tôi không sử dụng các "guard nodes" băng thông thấp
- Chúng tôi sử dụng các tunnel pools bao gồm nhiều tunnel, và lưu lượng có thể chuyển từ tunnel này sang tunnel khác.
- Các tunnel không tồn tại lâu dài; tunnel mới được xây dựng mỗi 10 phút.
- Độ dài tunnel có thể cấu hình được. Mặc dù tunnel 3-hop được khuyến nghị để bảo vệ đầy đủ, một số ứng dụng và dịch vụ sử dụng tunnel 2-hop theo mặc định.

Trong tương lai, có thể sẽ khả thi cho các peer có thể chấp nhận độ trễ đáng kể (theo các chiến lược trì hoãn và xử lý theo lô không tầm thường). Ngoài ra, điều này chỉ có liên quan đến các destination mà người khác biết về — một nhóm riêng tư có destination chỉ được biết bởi các peer đáng tin cậy thì không cần lo lắng, vì kẻ tấn công không thể "ping" họ để thực hiện cuộc tấn công.

Tham khảo: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Các cuộc tấn công từ chối dịch vụ

Có rất nhiều cuộc tấn công từ chối dịch vụ có thể thực hiện chống lại I2P, mỗi loại đều có chi phí và hậu quả khác nhau:

**Tấn công người dùng tham lam:** Đây đơn giản là những người cố gắng tiêu thụ nhiều tài nguyên hơn đáng kể so với những gì họ sẵn sàng đóng góp. Biện pháp phòng thủ chống lại điều này là:

- Đặt cài đặt mặc định để hầu hết người dùng cung cấp tài nguyên cho mạng. Trong I2P, người dùng định tuyến lưu lượng theo mặc định. Khác biệt rõ rệt với [các mạng khác](/docs/overview/comparison/), hơn 95% người dùng I2P chuyển tiếp lưu lượng cho người khác.
- Cung cấp các tùy chọn cấu hình dễ dàng để người dùng có thể tăng cường đóng góp (tỷ lệ chia sẻ) cho mạng. Hiển thị các chỉ số dễ hiểu như "tỷ lệ chia sẻ" để người dùng có thể thấy những gì họ đang đóng góp.
- Duy trì một cộng đồng mạnh mẽ với blog, diễn đàn, IRC và các phương tiện giao tiếp khác.

**Tấn công bỏ đói:** Một người dùng thù địch có thể cố gắng gây hại cho mạng lưới bằng cách tạo ra một số lượng lớn các peer trong mạng mà không bị nhận diện là đang dưới sự kiểm soát của cùng một thực thể (như với Sybil). Những node này sau đó quyết định không cung cấp bất kỳ tài nguyên nào cho mạng lưới, khiến các peer hiện có phải tìm kiếm thông qua cơ sở dữ liệu mạng lớn hơn hoặc yêu cầu nhiều tunnel hơn mức cần thiết. Ngoài ra, các node có thể cung cấp dịch vụ không ổn định bằng cách định kỳ loại bỏ lưu lượng được chọn, hoặc từ chối kết nối đến một số peer nhất định. Hành vi này có thể không thể phân biệt được với hành vi của một node bị tải nặng hoặc đang lỗi. I2P giải quyết những vấn đề này bằng cách duy trì hồ sơ về các peer, cố gắng xác định những peer hoạt động kém và đơn giản là bỏ qua chúng, hoặc sử dụng chúng rất ít. Chúng tôi đã cải thiện đáng kể khả năng nhận diện và tránh các peer có vấn đề; tuy nhiên vẫn còn những nỗ lực đáng kể cần thiết trong lĩnh vực này.

**Tấn công flooding:** Một người dùng thù địch có thể cố gắng flooding mạng lưới, một peer, một đích đến, hoặc một tunnel. Việc flooding mạng lưới và peer là có thể xảy ra, và I2P không làm gì để ngăn chặn các cuộc tấn công flooding ở lớp IP tiêu chuẩn. Việc flooding một đích đến bằng các tin nhắn thông qua việc gửi một lượng lớn đến các gateway tunnel đầu vào khác nhau của mục tiêu là có thể, nhưng đích đến sẽ biết được điều này cả từ nội dung của tin nhắn và vì các bài kiểm tra của tunnel sẽ thất bại. Điều tương tự cũng xảy ra khi flooding chỉ một tunnel duy nhất. I2P không có biện pháp phòng vệ nào cho cuộc tấn công flooding mạng lưới. Đối với tấn công flooding đích đến và tunnel, mục tiêu xác định những tunnel nào không phản hồi và xây dựng những tunnel mới. Mã nguồn mới cũng có thể được viết để thêm nhiều tunnel hơn nữa nếu client muốn xử lý tải lớn hơn. Mặt khác, nếu tải nhiều hơn khả năng mà client có thể xử lý, họ có thể chỉ thị cho các tunnel điều chỉnh số lượng tin nhắn hoặc byte mà chúng nên chuyển tiếp (một khi hoạt động tunnel nâng cao được triển khai).

**Tấn công tải CPU:** Hiện tại có một số phương thức cho phép mọi người yêu cầu từ xa một peer thực hiện các thao tác mã hóa tốn kém, và kẻ tấn công thù địch có thể sử dụng chúng để làm ngập peer đó với một số lượng lớn các yêu cầu nhằm cố gắng quá tải CPU. Cả việc sử dụng các thực hành kỹ thuật tốt và có thể yêu cầu các chứng chỉ không tầm thường (ví dụ: HashCash) được đính kèm vào những yêu cầu tốn kém này sẽ giúp giảm thiểu vấn đề, mặc dù vẫn có thể có chỗ để kẻ tấn công khai thác các lỗi khác nhau trong quá trình triển khai.

**Tấn công DOS floodfill:** Một người dùng thù địch có thể cố gắng làm hại mạng lưới bằng cách trở thành một floodfill router. Các biện pháp phòng thủ hiện tại chống lại các floodfill router không đáng tin cậy, không ổn định, hoặc độc hại vẫn còn yếu. Một floodfill router có thể cung cấp phản hồi xấu hoặc không phản hồi cho các truy vấn, và nó cũng có thể can thiệp vào việc giao tiếp giữa các floodfill. Một số biện pháp phòng thủ và profiling peer đã được triển khai, tuy nhiên vẫn còn rất nhiều việc cần làm. Để biết thêm thông tin, xem [trang network database](/docs/specs/common-structures/).

### Tấn Công Gắn Thẻ

Các cuộc tấn công gắn thẻ — sửa đổi một thông điệp để có thể nhận diện nó sau này trên đường truyền — về bản chất là không thể thực hiện được trong I2P, vì các thông điệp được truyền qua tunnel đều được ký số. Tuy nhiên, nếu kẻ tấn công vừa là inbound tunnel gateway vừa là một thành viên tham gia khác trong cùng tunnel đó, thông qua sự câu kết họ có thể xác định được sự thật rằng họ đang ở trong cùng một tunnel (và trước khi bổ sung các hop id duy nhất cùng các cập nhật khác, những peer câu kết trong cùng một tunnel có thể nhận ra sự thật này mà không cần bất kỳ nỗ lực nào). Tuy nhiên, một kẻ tấn công trong outbound tunnel và bất kỳ phần nào của inbound tunnel không thể câu kết với nhau, vì mã hóa tunnel sẽ đệm và sửa đổi dữ liệu riêng biệt cho inbound và outbound tunnel. Các kẻ tấn công bên ngoài không thể làm gì, vì các liên kết được mã hóa và thông điệp được ký số.

### Các Cuộc Tấn Công Phân Vùng

Các cuộc tấn công phân vùng — tìm cách để tách biệt (về mặt kỹ thuật hoặc phân tích) các peer trong một mạng — là điều quan trọng cần ghi nhớ khi đối phó với một đối thủ mạnh, vì kích thước của mạng đóng vai trò then chốt trong việc xác định tính ẩn danh của bạn. Việc phân vùng kỹ thuật bằng cách cắt đứt các liên kết giữa các peer để tạo ra các mạng phân mảnh được I2P giải quyết thông qua netDb tích hợp, duy trì thống kê về các peer khác nhau để cho phép bất kỳ kết nối hiện có nào đến các phần phân mảnh khác có thể được khai thác nhằm khôi phục mạng. Tuy nhiên, nếu kẻ tấn công thực sự ngắt tất cả các liên kết đến các peer không được kiểm soát, về cơ bản là cô lập mục tiêu, thì không có cách khôi phục netDb nào có thể sửa chữa được. Tại thời điểm đó, điều duy nhất mà router có thể hy vọng làm là nhận ra rằng một số lượng đáng kể các peer đáng tin cậy trước đây đã trở nên không khả dụng và cảnh báo client rằng nó tạm thời bị ngắt kết nối (mã phát hiện này hiện chưa được triển khai).

Việc phân vùng mạng một cách phân tích bằng cách tìm kiếm sự khác biệt trong cách các router và đích đến hoạt động và nhóm chúng tương ứng cũng là một cuộc tấn công rất mạnh mẽ. Ví dụ, một kẻ tấn công [thu thập](#harvesting-attacks) cơ sở dữ liệu mạng sẽ biết khi nào một đích đến cụ thể có 5 tunnel đến trong LeaseSet của họ trong khi các đích khác chỉ có 2 hoặc 3, cho phép đối thủ có khả năng phân vùng các client theo số lượng tunnel được chọn. Một phân vùng khác có thể xảy ra khi xử lý các chiến lược trì hoãn và xử lý theo lô không tầm thường, vì các cổng vào tunnel và các hop cụ thể với độ trì hoãn khác không có thể sẽ nổi bật. Tuy nhiên, dữ liệu này chỉ được tiết lộ cho những hop cụ thể đó, vì vậy để phân vùng hiệu quả về vấn đề này, kẻ tấn công sẽ cần kiểm soát một phần đáng kể của mạng (và vẫn chỉ là một phân vùng xác suất, vì họ sẽ không biết tunnel hoặc tin nhắn nào khác có những độ trì hoãn đó).

Cũng được thảo luận trên [trang network database](/docs/specs/common-structures/) (tấn công bootstrap).

### Tấn công Tiền nhiệm

Cuộc tấn công predecessor là việc thu thập thống kê một cách thụ động nhằm cố gắng xem những peer nào "gần" với đích đến bằng cách tham gia vào các tunnel của họ và theo dõi hop trước hoặc hop tiếp theo (tương ứng với outbound hoặc inbound tunnel). Theo thời gian, bằng cách sử dụng một mẫu hoàn toàn ngẫu nhiên các peer và thứ tự ngẫu nhiên, kẻ tấn công có thể thấy peer nào xuất hiện "gần hơn" về mặt thống kê so với những peer còn lại, và peer đó sẽ là nơi mục tiêu được định vị.

I2P tránh điều này bằng bốn cách: thứ nhất, các peer được chọn để tham gia vào tunnel không được lấy mẫu ngẫu nhiên trên toàn mạng — chúng được tạo ra từ thuật toán lựa chọn peer chia chúng thành các tầng. Thứ hai, với [strict ordering](/docs/specs/tunnel-implementation/#ordering) của các peer trong một tunnel, việc một peer xuất hiện thường xuyên hơn không có nghĩa là chúng là nguồn. Thứ ba, với độ dài tunnel được hoán vị (không được bật theo mặc định), ngay cả tunnel 0 hop cũng có thể cung cấp khả năng phủ nhận hợp lý vì sự thay đổi thỉnh thoảng của gateway sẽ trông giống như các tunnel bình thường. Thứ tư, với restricted routes (chưa được triển khai), chỉ peer có kết nối bị hạn chế đến đích mới liên lạc với đích, trong khi những kẻ tấn công sẽ chỉ gặp phải gateway đó.

Phương pháp xây dựng tunnel hiện tại được thiết kế đặc biệt để chống lại cuộc tấn công predecessor. Xem thêm [cuộc tấn công giao điểm](#intersection-attacks).

Tài liệu tham khảo: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), là bản cập nhật của [bài báo tấn công tiền nhiệm năm 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf).

### Các Cuộc Tấn Công Thu Thập

"Harvesting" có nghĩa là biên soạn danh sách các người dùng đang chạy I2P. Nó có thể được sử dụng cho các cuộc tấn công pháp lý và hỗ trợ các cuộc tấn công khác bằng cách đơn giản là chạy một peer, quan sát xem nó kết nối với ai, và thu thập bất kỳ tham chiếu nào đến các peer khác mà nó có thể tìm thấy.

Bản thân I2P không được thiết kế với các biện pháp phòng thủ hiệu quả chống lại cuộc tấn công này, vì có cơ sở dữ liệu mạng phân tán chứa chính thông tin này. Các yếu tố sau đây làm cho cuộc tấn công trở nên khó khăn hơn trong thực tế:

- Sự tăng trưởng của mạng sẽ khiến việc chiếm được một tỷ lệ nhất định của mạng trở nên khó khăn hơn
- Các floodfill router thực hiện giới hạn truy vấn như một biện pháp bảo vệ chống DOS
- "Chế độ ẩn", ngăn không cho router công bố thông tin của nó lên netDb (nhưng cũng ngăn nó chuyển tiếp dữ liệu) hiện không được sử dụng rộng rãi nhưng có thể sẽ được sử dụng.

Trong các triển khai tương lai, các tuyến đường hạn chế cơ bản và toàn diện sẽ giảm sức mạnh của cuộc tấn công này, vì các peer "ẩn" không công bố địa chỉ liên lạc của họ trong cơ sở dữ liệu mạng — chỉ công bố các tunnel mà qua đó chúng có thể được tiếp cận (cũng như khóa công khai của chúng, v.v.).

Trong tương lai, các router có thể sử dụng GeoIP để xác định xem chúng có đang ở một quốc gia cụ thể nào đó mà việc bị nhận diện là một I2P node sẽ có rủi ro hay không. Trong trường hợp đó, router có thể tự động kích hoạt chế độ ẩn, hoặc thực hiện các phương pháp định tuyến hạn chế khác.

### Nhận dạng thông qua phân tích lưu lượng

Bằng cách kiểm tra lưu lượng truy cập vào và ra khỏi một router, một ISP độc hại hoặc tường lửa cấp nhà nước có thể xác định rằng một máy tính đang chạy I2P. Như đã thảo luận [ở trên](#harvesting-attacks), I2P không được thiết kế đặc biệt để ẩn việc một máy tính đang chạy I2P. Tuy nhiên, một số quyết định thiết kế được đưa ra trong thiết kế của tầng vận chuyển và các giao thức làm cho việc xác định lưu lượng I2P trở nên khó khăn một chút:

- Lựa chọn cổng ngẫu nhiên
- Mã hóa điểm-đến-điểm cho toàn bộ lưu lượng
- Trao đổi khóa DH không có byte giao thức hoặc các trường hằng số không được mã hóa khác
- Sử dụng đồng thời cả hai giao thức truyền tải TCP và UDP. UDP có thể khó theo dõi hơn nhiều đối với một số thiết bị Deep Packet Inspection (DPI).

Trong tương lai gần, chúng tôi dự định giải quyết trực tiếp các vấn đề phân tích lưu lượng bằng cách làm mơ hồ thêm các giao thức truyền tải I2P, có thể bao gồm:

- Padding ở lớp transport với độ dài ngẫu nhiên, đặc biệt trong quá trình bắt tay kết nối
- Nghiên cứu đặc điểm phân bố kích thước gói tin và thêm padding khi cần thiết
- Phát triển các phương thức transport bổ sung mô phỏng SSL hoặc các giao thức phổ biến khác
- Xem xét các chiến lược padding ở các lớp cao hơn để hiểu cách chúng ảnh hưởng đến kích thước gói tin ở lớp transport
- Xem xét các phương pháp được triển khai bởi các tường lửa cấp nhà nước để chặn Tor
- Làm việc trực tiếp với các chuyên gia DPI và obfuscation

Tham khảo: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Tấn công Sybil

Sybil mô tả một loại tấn công trong đó kẻ thù tạo ra số lượng lớn tùy ý các node cùng thông đồng và sử dụng số lượng tăng lên để hỗ trợ thực hiện các cuộc tấn công khác. Ví dụ, nếu kẻ tấn công ở trong một mạng lưới nơi các peer được chọn ngẫu nhiên và họ muốn có 80% cơ hội trở thành một trong những peer đó, họ chỉ cần tạo ra gấp năm lần số lượng node có trong mạng và thử vận may. Khi danh tính miễn phí, Sybil có thể là một kỹ thuật rất mạnh mẽ đối với kẻ thù có khả năng. Kỹ thuật chính để giải quyết vấn đề này đơn giản là làm cho danh tính 'không miễn phí' — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (cùng với các hệ thống khác) sử dụng thực tế là địa chỉ IP bị giới hạn, trong khi IIP sử dụng [HashCash](http://www.hashcash.org/) để 'tính phí' cho việc tạo danh tính mới. Hiện tại chúng tôi chưa triển khai bất kỳ kỹ thuật cụ thể nào để giải quyết Sybil, nhưng có bao gồm các chứng chỉ giữ chỗ trong cấu trúc dữ liệu của router và destination có thể chứa chứng chỉ HashCash với giá trị thích hợp khi cần thiết (hoặc một số chứng chỉ khác chứng minh tính khan hiếm).

Việc yêu cầu Chứng chỉ HashCash ở nhiều nơi khác nhau có hai vấn đề chính:

- Duy trì khả năng tương thích ngược
- Vấn đề HashCash cổ điển — lựa chọn các giá trị HashCash có ý nghĩa như bằng chứng công việc trên các máy cao cấp, trong khi vẫn khả thi trên các máy cấu hình thấp như thiết bị di động.

Các hạn chế khác nhau về số lượng router trong một dải IP nhất định giúp hạn chế lỗ hổng đối với những kẻ tấn công không có khả năng đặt máy trong nhiều khối IP. Tuy nhiên, đây không phải là một biện pháp phòng thủ có ý nghĩa chống lại một đối thủ mạnh.

Xem [trang cơ sở dữ liệu mạng](/docs/specs/common-structures/) để thảo luận thêm về Sybil.

### Các Cuộc Tấn Công Kiệt Sức Buddy

(Tham khảo: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Phần 5.2)

Bằng cách từ chối chấp nhận hoặc chuyển tiếp các yêu cầu xây dựng tunnel, ngoại trừ đối với peer đồng lõa, một router có thể đảm bảo rằng tunnel được hình thành hoàn toàn từ tập hợp các router đồng lõa của nó. Khả năng thành công được tăng cường nếu có số lượng lớn các router đồng lõa, tức là một [cuộc tấn công Sybil](#sybil-attacks). Điều này được giảm thiểu phần nào bằng các phương pháp profiling peer (lập hồ sơ ngang hàng) của chúng ta được sử dụng để giám sát hiệu suất của các peer. Tuy nhiên, đây là một cuộc tấn công mạnh mẽ khi số lượng router tiến gần đến *f* = 0.2, hoặc 20% node độc hại, như được chỉ định trong bài báo. Các router độc hại cũng có thể duy trì kết nối với router mục tiêu và cung cấp băng thông chuyển tiếp xuất sắc cho lưu lượng qua những kết nối đó, trong nỗ lực thao túng các hồ sơ được quản lý bởi mục tiêu và có vẻ hấp dẫn. Có thể cần thiết nghiên cứu và phòng thủ thêm.

### Các Cuộc Tấn Công Mật Mã

Chúng tôi sử dụng mã hóa mạnh với các khóa dài, và chúng tôi giả định tính bảo mật của các nguyên thủy mã hóa tiêu chuẩn công nghiệp được sử dụng trong I2P. Các tính năng bảo mật bao gồm việc phát hiện ngay lập tức các thông điệp bị thay đổi dọc theo đường đi, khả năng không thể giải mã các thông điệp không được gửi cho bạn, và phòng thủ chống lại các cuộc tấn công man-in-the-middle. Kích thước khóa được chọn vào năm 2003 khá thận trọng vào thời điểm đó, và vẫn dài hơn so với những khóa được sử dụng trong [các mạng ẩn danh khác](https://torproject.org/). Chúng tôi không nghĩ rằng độ dài khóa hiện tại là điểm yếu lớn nhất của chúng tôi, đặc biệt đối với các đối thủ truyền thống, không ở cấp độ nhà nước; lỗi và quy mô nhỏ của mạng lưới mới đáng lo ngại hơn nhiều. Tất nhiên, tất cả các thuật toán mã hóa cuối cùng đều trở nên lỗi thời do sự ra đời của các bộ xử lý nhanh hơn, nghiên cứu mã hóa, và tiến bộ trong các phương pháp như bảng rainbow, cụm phần cứng trò chơi điện tử, v.v. Thật không may, I2P không được thiết kế với các cơ chế dễ dàng để kéo dài khóa hoặc thay đổi các giá trị bí mật chia sẻ trong khi vẫn duy trì khả năng tương thích ngược.

Việc nâng cấp các cấu trúc dữ liệu và giao thức khác nhau để hỗ trợ khóa dài hơn sẽ phải được giải quyết cuối cùng, và đây sẽ là một công việc lớn, giống như với [những dự án khác](https://torproject.org/). Hy vọng rằng, thông qua việc lập kế hoạch cẩn thận, chúng ta có thể giảm thiểu sự gián đoạn và triển khai các cơ chế để làm cho việc chuyển đổi trong tương lai trở nên dễ dàng hơn.

Trong tương lai, một số giao thức I2P và cấu trúc dữ liệu sẽ hỗ trợ việc đệm thông điệp một cách an toàn đến các kích thước tùy ý, do đó các thông điệp có thể được tạo với kích thước cố định hoặc các garlic message có thể được chỉnh sửa ngẫu nhiên để một số clove có vẻ chứa nhiều subclove hơn thực tế. Tuy nhiên, hiện tại các thông điệp garlic, tunnel và đầu-cuối-đầu bao gồm phần đệm ngẫu nhiên đơn giản.

### Các Cuộc Tấn Công Ẩn Danh Floodfill

Ngoài các cuộc tấn công DOS floodfill được mô tả [ở trên](#denial-of-service-attacks), các router floodfill có vị trí đặc biệt để thu thập thông tin về các thành viên trong mạng, do vai trò của chúng trong netDb và tần suất giao tiếp cao với các thành viên đó. Điều này được giảm thiểu phần nào vì các router floodfill chỉ quản lý một phần của tổng keyspace, và keyspace này được xoay vòng hàng ngày, như đã giải thích trên [trang cơ sở dữ liệu mạng](/docs/specs/common-structures/). Các cơ chế cụ thể mà các router giao tiếp với floodfill đã được thiết kế cẩn thận. Tuy nhiên, những mối đe dọa này cần được nghiên cứu thêm. Các mối đe dọa tiềm ẩn cụ thể và các biện pháp phòng vệ tương ứng là chủ đề cho nghiên cứu tương lai.

### Các Cuộc Tấn Công Cơ Sở Dữ Liệu Mạng Khác

Một người dùng thù địch có thể cố gắng làm hại mạng lưới bằng cách tạo một hoặc nhiều floodfill router và thiết kế chúng để đưa ra các phản hồi xấu, chậm hoặc không phản hồi. Một số kịch bản được thảo luận trên [trang network database](/docs/specs/common-structures/).

### Các Cuộc Tấn Công Tài Nguyên Trung Tâm

Có một số tài nguyên tập trung hoặc hạn chế (một số trong I2P, một số không) có thể bị tấn công hoặc được sử dụng như một vectơ tấn công. Việc jrandom vắng mặt từ tháng 11 năm 2007, tiếp theo là mất dịch vụ hosting i2p.net vào tháng 1 năm 2008, đã làm nổi bật nhiều tài nguyên tập trung trong quá trình phát triển và vận hành mạng I2P, phần lớn trong số đó hiện đã được phân tán. Các cuộc tấn công vào tài nguyên có thể tiếp cận từ bên ngoài chủ yếu ảnh hưởng đến khả năng người dùng mới tìm thấy chúng ta, chứ không phải hoạt động của chính mạng lưới.

- Trang web được nhân bản và sử dụng DNS round-robin để truy cập công khai từ bên ngoài.
- Các router hiện hỗ trợ [nhiều vị trí reseed bên ngoài](/docs/overview/faq/#reseed), tuy nhiên có thể cần thêm nhiều reseed host, và việc xử lý các reseed host không đáng tin cậy hoặc độc hại có thể cần được cải thiện.
- Các router hiện hỗ trợ nhiều vị trí file cập nhật. Một update host độc hại có thể cung cấp file rất lớn; cần giới hạn kích thước.
- Các router hiện hỗ trợ nhiều update signer được tin tưởng mặc định.
- Các router hiện xử lý tốt hơn nhiều floodfill peer không đáng tin cậy. Các floodfill độc hại cần được nghiên cứu thêm.
- Mã nguồn hiện được lưu trữ trong hệ thống kiểm soát nguồn phân tán.
- Các router phụ thuộc vào một news host duy nhất, nhưng có URL dự phòng được hardcode trỏ đến một host khác. Một news host độc hại có thể cung cấp file rất lớn; cần giới hạn kích thước.
- [Các dịch vụ hệ thống đặt tên](/docs/overview/naming/), bao gồm nhà cung cấp đăng ký address book, dịch vụ add-host, và dịch vụ jump, có thể là độc hại. Các biện pháp bảo vệ đáng kể cho subscriptions đã được triển khai trong phiên bản 0.6.1.31, với các cải tiến bổ sung trong các phiên bản tiếp theo. Tuy nhiên, tất cả naming services đều yêu cầu một mức độ tin tưởng nhất định; xem [trang naming](/docs/overview/naming/) để biết chi tiết.
- Chúng ta vẫn phụ thuộc vào dịch vụ DNS cho i2p2.de; việc mất điều này sẽ gây ra sự gián đoạn đáng kể trong khả năng thu hút người dùng mới, và sẽ làm thu hẹp mạng lưới (trong ngắn hạn đến trung hạn), giống như việc mất i2p.net đã từng xảy ra.

### Các Cuộc Tấn Công Phát Triển

Những cuộc tấn công này không nhắm trực tiếp vào mạng lưới, mà thay vào đó nhắm vào nhóm phát triển bằng cách đưa ra các rào cản pháp lý đối với bất kỳ ai đóng góp vào việc phát triển phần mềm, hoặc bằng cách sử dụng mọi phương tiện có sẵn để khiến các nhà phát triển phá hoại phần mềm. Các biện pháp kỹ thuật truyền thống không thể đánh bại những cuộc tấn công này, và nếu ai đó đe dọa tính mạng hoặc sinh kế của một nhà phát triển (hoặc thậm chí chỉ ban hành lệnh tòa án kèm với lệnh cấm tiết lộ, dưới sự đe dọa của tù tội), chúng ta sẽ gặp phải một vấn đề lớn.

Tuy nhiên, có hai kỹ thuật giúp phòng thủ chống lại các cuộc tấn công này:

- Tất cả các thành phần của mạng phải là mã nguồn mở để cho phép kiểm tra, xác minh, sửa đổi và cải tiến. Nếu một nhà phát triển bị xâm phạm, một khi điều này được phát hiện, cộng đồng nên yêu cầu giải thích và ngừng chấp nhận công việc của nhà phát triển đó. Tất cả các lần checkin vào hệ thống kiểm soát mã nguồn phân tán của chúng tôi đều được ký mã hóa, và các packager phát hành sử dụng hệ thống danh sách tin cậy để hạn chế các sửa đổi chỉ cho những người đã được phê duyệt trước đó.
- Phát triển qua chính mạng đó, cho phép các nhà phát triển giữ ẩn danh nhưng vẫn bảo mật quá trình phát triển. Tất cả việc phát triển I2P có thể diễn ra thông qua I2P — sử dụng hệ thống kiểm soát mã nguồn phân tán, chat IRC, máy chủ web công khai, diễn đàn thảo luận (forum.i2p), và các trang phân phối phần mềm, tất cả đều có sẵn trong I2P.

Chúng tôi cũng duy trì mối quan hệ với các tổ chức khác nhau cung cấp tư vấn pháp lý, trong trường hợp cần thiết phải bảo vệ.

### Các Cuộc Tấn Công Thực Hiện (Lỗi)

Dù chúng tôi cố gắng đến đâu, hầu hết các ứng dụng phức tạp đều chứa lỗi trong thiết kế hoặc triển khai, và I2P cũng không ngoại lệ. Có thể tồn tại những lỗi có thể bị khai thác để tấn công tính ẩn danh hoặc bảo mật của việc truyền thông qua I2P theo những cách không lường trước được. Để giúp chống chịu các cuộc tấn công vào thiết kế hoặc giao thức đang sử dụng, chúng tôi công bố tất cả các thiết kế và tài liệu cũng như yêu cầu xem xét và phê bình với hy vọng rằng nhiều ánh mắt sẽ cải thiện hệ thống. Chúng tôi không tin vào bảo mật thông qua che giấu.

Ngoài ra, mã nguồn cũng được đối xử theo cách tương tự, với ít sự ngại ngần trong việc tái cấu trúc hoặc loại bỏ những phần không đáp ứng được nhu cầu của hệ thống phần mềm (bao gồm cả tính dễ dàng thay đổi). Tài liệu về thiết kế và triển khai mạng lưới cũng như các thành phần phần mềm là một phần thiết yếu của bảo mật, vì thiếu chúng thì các nhà phát triển khó có thể sẵn sàng dành thời gian để tìm hiểu phần mềm đủ sâu để xác định các điểm yếu và lỗi.

Phần mềm của chúng tôi có khả năng, đặc biệt, chứa các lỗi liên quan đến tấn công từ chối dịch vụ thông qua lỗi hết bộ nhớ (OOM), các vấn đề cross-site-scripting (XSS) trong router console, và các lỗ hổng bảo mật khác đối với các đầu vào không chuẩn qua các giao thức khác nhau.

I2P vẫn là một mạng lưới nhỏ với cộng đồng phát triển ít ỏi và gần như không có sự quan tâm từ các nhóm học thuật hay nghiên cứu. Do đó chúng tôi thiếu các phân tích mà [các mạng ẩn danh khác](https://torproject.org/) có thể đã nhận được. Chúng tôi tiếp tục tuyển dụng mọi người để [tham gia](/get-involved/) và hỗ trợ.

---

## Các Biện Pháp Bảo Vệ Khác

### Danh sách chặn

Ở một mức độ nào đó, I2P có thể được cải tiến để tránh các peer hoạt động tại các địa chỉ IP được liệt kê trong danh sách chặn. Một số danh sách chặn thường có sẵn ở các định dạng tiêu chuẩn, liệt kê các tổ chức chống P2P, các đối thủ tiềm năng ở cấp độ nhà nước và những đối tượng khác.

Trong phạm vi mà các peer hoạt động thực sự xuất hiện trong blocklist thực tế, việc chặn chỉ bởi một tập hợp con của các peer sẽ có xu hướng phân đoạn mạng, làm trầm trọng thêm các vấn đề về khả năng kết nối và giảm độ tin cậy tổng thể. Do đó chúng ta sẽ muốn thống nhất về một blocklist cụ thể và bật nó theo mặc định.

Blocklist chỉ là một phần (có thể là phần nhỏ) trong một loạt các biện pháp phòng thủ chống lại các hành vi độc hại. Phần lớn hệ thống profiling hoạt động tốt trong việc đo lường hành vi router để chúng ta không cần phải tin tưởng bất cứ thứ gì trong netDb. Tuy nhiên vẫn có thể làm được nhiều hơn nữa. Đối với mỗi lĩnh vực trong danh sách trên, chúng ta có thể cải thiện trong việc phát hiện các hành vi xấu.

Nếu một danh sách chặn được lưu trữ tại một vị trí trung tâm với cập nhật tự động thì mạng lưới sẽ dễ bị tấn công bởi [tấn công tài nguyên trung tâm](#central-resource-attacks). Việc đăng ký tự động vào một danh sách sẽ trao cho nhà cung cấp danh sách quyền lực để tắt toàn bộ mạng I2P. Hoàn toàn.

Hiện tại, một blocklist mặc định được phân phối cùng với phần mềm của chúng tôi, chỉ liệt kê các IP của các nguồn DOS trong quá khứ. Không có cơ chế cập nhật tự động. Nếu một dải IP cụ thể thực hiện các cuộc tấn công nghiêm trọng vào mạng I2P, chúng tôi sẽ phải yêu cầu mọi người cập nhật blocklist của họ một cách thủ công thông qua các cơ chế ngoài băng tần như diễn đàn, blog, v.v.
