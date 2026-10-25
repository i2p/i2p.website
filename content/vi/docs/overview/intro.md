---
title: "I2P: Một Framework Có Thể Mở Rộng Cho Giao Tiếp Ẩn Danh"
description: "Giới thiệu về kiến trúc và hoạt động của I2P"
slug: "intro"
aliases:
  - "/vi/intro"
  - "/vi/intro/"
  - "/vi/how_intro"
  - "/vi/how_intro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

LƯU Ý: Tài liệu này được viết lần đầu bởi jrandom vào năm 2003. Mặc dù chúng tôi nỗ lực cập nhật thông tin, một số thông tin có thể đã lỗi thời hoặc chưa đầy đủ. Các phần transport và cryptography được cập nhật tính đến tháng 01-2025.

## Giới thiệu

I2P là một lớp mạng ẩn danh chuyển mạch gói tin có khả năng mở rộng, tự tổ chức và kiên cường, trên đó có thể hoạt động bất kỳ số lượng ứng dụng nào quan tâm đến tính ẩn danh hoặc bảo mật. Mỗi ứng dụng này có thể đưa ra những đánh đổi riêng về tính ẩn danh, độ trễ và thông lượng mà không cần lo lắng về việc triển khai đúng đắn một mixnet tuyến đường tự do, cho phép chúng hòa trộn hoạt động của mình với tập hợp ẩn danh lớn hơn của những người dùng đã đang chạy trên I2P.

Các ứng dụng hiện có đã cung cấp đầy đủ các hoạt động Internet thông thường — duyệt web **ẩn danh**, lưu trữ web, trò chuyện, chia sẻ tệp, email, viết blog và phân phối nội dung, cũng như một số ứng dụng khác đang trong quá trình phát triển.

- Duyệt web: sử dụng bất kỳ trình duyệt hiện có nào hỗ trợ sử dụng proxy.
- Trò chuyện: IRC và các giao thức khác
- Chia sẻ tệp: [I2PSnark](#i2psnark) và các ứng dụng khác
- E-mail: [susimail](#i2pmail--susimail) và các ứng dụng khác
- Blog: sử dụng bất kỳ máy chủ web cục bộ nào, hoặc các plugin có sẵn

Khác với các trang web được lưu trữ trong các mạng phân phối nội dung như [Freenet](#freenet) hoặc [GNUnet](https://www.gnunet.org/en/), các dịch vụ được lưu trữ trên I2P có tính tương tác đầy đủ — có các công cụ tìm kiếm kiểu web truyền thống, bảng tin, blog mà bạn có thể bình luận, các trang web điều khiển bằng cơ sở dữ liệu, và các cầu nối để truy vấn các hệ thống tĩnh như Freenet mà không cần cài đặt cục bộ.

Với tất cả các ứng dụng bảo mật ẩn danh này, I2P đóng vai trò như một middleware hướng thông điệp — các ứng dụng chỉ cần nói rằng chúng muốn gửi một số dữ liệu đến một định danh mật mã (một "destination") và I2P sẽ đảm bảo việc truyền tải được thực hiện một cách an toàn và ẩn danh. I2P cũng tích hợp một [thư viện streaming](#streaming-library) đơn giản để cho phép các thông điệp tối ưu nỗ lực ẩn danh của I2P có thể truyền tải dưới dạng các luồng đáng tin cậy, có thứ tự, đồng thời cung cấp minh bạch thuật toán kiểm soát tắc nghẽn dựa trên TCP được điều chỉnh cho sản phẩm độ trễ băng thông cao của mạng. Mặc dù đã có một số SOCKS proxy đơn giản có sẵn để kết nối các ứng dụng hiện có vào mạng, giá trị của chúng bị hạn chế vì hầu như mọi ứng dụng thường xuyên tiết lộ những thông tin trong bối cảnh ẩn danh được coi là nhạy cảm. Cách duy nhất an toàn là kiểm tra toàn diện một ứng dụng để đảm bảo hoạt động đúng cách và để hỗ trợ việc đó, chúng tôi cung cấp một loạt các API bằng nhiều ngôn ngữ khác nhau có thể được sử dụng để tận dụng tối đa mạng.

I2P không phải là một dự án nghiên cứu — học thuật, thương mại, hay chính phủ — mà thay vào đó là một nỗ lực kỹ thuật nhằm làm bất cứ điều gì cần thiết để cung cấp mức độ ẩn danh đầy đủ cho những người cần nó. Nó đã được phát triển tích cực từ đầu năm 2003 với một nhà phát triển toàn thời gian và một nhóm tận tụy các cộng tác viên bán thời gian từ khắp nơi trên thế giới. Tất cả công việc được thực hiện trên I2P đều là mã nguồn mở và có sẵn miễn phí trên [website](/), với phần lớn mã được phát hành thẳng vào phạm vi công cộng, mặc dù có sử dụng một số thủ tục mật mã dưới giấy phép kiểu BSD. Những người làm việc trên I2P không kiểm soát việc mọi người phát hành ứng dụng client dưới giấy phép gì, và có một số ứng dụng GPL có sẵn ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex và những ứng dụng khác). Kinh phí cho I2P hoàn toàn đến từ quyên góp, và không nhận được bất kỳ ưu đãi thuế nào ở bất cứ khu vực pháp lý nào vào thời điểm này, vì nhiều nhà phát triển bản thân cũng ẩn danh.

---

## Vận hành

### Tổng quan

Để hiểu hoạt động của I2P, điều cần thiết là phải hiểu một số khái niệm chính. Đầu tiên, I2P tách bạch nghiêm ngặt giữa phần mềm tham gia vào mạng (một "router") và các điểm cuối ẩn danh ("destinations") được liên kết với các ứng dụng riêng lẻ. Việc ai đó đang chạy I2P thường không phải là bí mật. Điều được ẩn giấu là thông tin về những gì người dùng đang làm, nếu có, cũng như router nào mà một destination cụ thể đang kết nối. Người dùng cuối thường sẽ có một số destinations cục bộ trên router của họ — ví dụ, một để proxy vào các máy chủ IRC, một khác hỗ trợ máy chủ web ẩn danh của người dùng ("I2P Site"), một khác cho phiên bản I2Phex, một khác cho torrents, v.v.

Một khái niệm quan trọng khác cần hiểu là "tunnel". Một tunnel là một đường dẫn có hướng thông qua một danh sách các router được chọn rõ ràng. Mã hóa nhiều lớp được sử dụng, do đó mỗi router chỉ có thể giải mã một lớp duy nhất. Thông tin đã giải mã chứa IP của router tiếp theo, cùng với thông tin được mã hóa cần được chuyển tiếp. Mỗi tunnel có một điểm bắt đầu (router đầu tiên, còn được gọi là "gateway") và một điểm kết thúc. Tin nhắn chỉ có thể được gửi theo một chiều. Để gửi tin nhắn trở lại, cần có một tunnel khác.

![Sơ đồ tunnel đến và đi](/images/tunnels.png) *Hình 1: Có hai loại tunnel: đến và đi.*

Có hai loại tunnel tồn tại: **"outbound tunnels"** gửi tin nhắn ra khỏi người tạo tunnel, trong khi **"inbound tunnels"** đưa tin nhắn đến người tạo tunnel. Kết hợp hai loại tunnel này cho phép người dùng gửi tin nhắn cho nhau. Người gửi ("Alice" trong hình trên) thiết lập một outbound tunnel, trong khi người nhận ("Bob" trong hình trên) tạo một inbound tunnel. Gateway của inbound tunnel có thể nhận tin nhắn từ bất kỳ người dùng nào khác và sẽ gửi chúng tiếp tục cho đến endpoint ("Bob"). Endpoint của outbound tunnel sẽ cần gửi tin nhắn đến gateway của inbound tunnel. Để làm điều này, người gửi ("Alice") thêm hướng dẫn vào tin nhắn được mã hóa của mình. Một khi endpoint của outbound tunnel giải mã tin nhắn, nó sẽ có hướng dẫn để chuyển tiếp tin nhắn đến đúng inbound gateway (gateway đến "Bob").

Một khái niệm quan trọng thứ ba cần hiểu là **"network database"** (hay "netDb") của I2P — một cặp thuật toán được sử dụng để chia sẻ siêu dữ liệu mạng. Hai loại siêu dữ liệu được truyền tải là **"routerInfo"** và **"leaseSets"** — routerInfo cung cấp cho các router dữ liệu cần thiết để liên lạc với một router cụ thể (khóa công khai, địa chỉ truyền tải, v.v.), trong khi leaseSet cung cấp cho các router thông tin cần thiết để liên lạc với một đích cụ thể. Một leaseSet chứa một số "lease". Mỗi lease này chỉ định một tunnel gateway, cho phép tiếp cận một đích cụ thể. Thông tin đầy đủ có trong một lease:

- Gateway đầu vào cho một tunnel cho phép tiếp cận một đích cụ thể.
- Thời gian khi một tunnel hết hạn.
- Cặp khóa công khai để có thể mã hóa tin nhắn (để gửi qua tunnel và tiếp cận đích).

Các router tự gửi routerInfo của chúng trực tiếp đến netDb, trong khi các leaseSet được gửi thông qua các tunnel đi ra (leaseSet cần được gửi một cách ẩn danh để tránh việc liên kết một router với các leaseSet của nó).

Chúng ta có thể kết hợp các khái niệm trên để xây dựng các kết nối thành công trong mạng.

Để xây dựng các tunnel đến và đi của riêng mình, Alice thực hiện tra cứu trong netDb để thu thập routerInfo. Bằng cách này, cô ấy tập hợp danh sách các peer mà cô có thể sử dụng làm hop trong các tunnel của mình. Sau đó cô có thể gửi thông điệp xây dựng đến hop đầu tiên, yêu cầu xây dựng tunnel và đề nghị router đó gửi tiếp thông điệp xây dựng, cho đến khi tunnel được xây dựng hoàn tất.

![Yêu cầu thông tin về các router khác](/images/netdb_get_routerinfo_1.png)

![Build tunnel using router information](/images/netdb_get_routerinfo_2.png) *Hình 2: Thông tin router được sử dụng để xây dựng tunnel.*

Khi Alice muốn gửi tin nhắn cho Bob, đầu tiên cô ấy thực hiện tra cứu trong netDb để tìm leaseSet của Bob, cho cô ấy các gateway tunnel đầu vào hiện tại của anh ấy. Sau đó cô ấy chọn một trong các outbound tunnel của mình và gửi tin nhắn xuống đó với hướng dẫn cho endpoint của outbound tunnel chuyển tiếp tin nhắn đến một trong các gateway tunnel đầu vào của Bob. Khi endpoint của outbound tunnel nhận được những hướng dẫn đó, nó chuyển tiếp tin nhắn theo yêu cầu, và khi gateway tunnel đầu vào của Bob nhận được nó, tin nhắn được chuyển tiếp xuống tunnel đến router của Bob. Nếu Alice muốn Bob có thể trả lời tin nhắn, cô ấy cần truyền đích đến của chính mình một cách rõ ràng như một phần của chính tin nhắn đó. Điều này có thể được thực hiện bằng cách giới thiệu một lớp cấp cao hơn, được thực hiện trong thư viện [streaming](#streaming-library). Alice cũng có thể giảm thời gian phản hồi bằng cách đính kèm LeaseSet mới nhất của mình với tin nhắn để Bob không cần thực hiện tra cứu netDb khi anh ấy muốn trả lời, nhưng điều này là tùy chọn.

![Connect tunnels using LeaseSets](/images/netdb_get_leaseset.png) *Hình 3: LeaseSets được sử dụng để kết nối các tunnel đi và tunnel đến.*

Trong khi bản thân các tunnel có mã hóa nhiều lớp để ngăn chặn việc tiết lộ trái phép cho các peer bên trong mạng (như chính lớp vận chuyển cũng làm để ngăn chặn việc tiết lộ trái phép cho các peer bên ngoài mạng), cần thiết phải thêm một lớp mã hóa đầu cuối bổ sung để ẩn thông điệp khỏi điểm cuối tunnel outbound và gateway tunnel inbound. "[Garlic encryption](#garlic-messages)" này cho phép router của Alice gói nhiều thông điệp thành một "garlic message" duy nhất, được mã hóa bằng một public key cụ thể để các peer trung gian không thể xác định có bao nhiêu thông điệp trong garlic, những thông điệp đó nói gì, hoặc các clove riêng lẻ được gửi đến đâu. Đối với giao tiếp đầu cuối điển hình giữa Alice và Bob, garlic sẽ được mã hóa bằng public key được xuất bản trong leaseSet của Bob, cho phép thông điệp được mã hóa mà không cần đưa public key cho router của chính Bob.

Một điều quan trọng khác cần ghi nhớ là I2P hoàn toàn dựa trên message và một số message có thể bị mất trên đường truyền. Các ứng dụng sử dụng I2P có thể dùng các giao diện hướng message và tự xử lý nhu cầu kiểm soát tắc nghẽn và độ tin cậy của riêng mình, nhưng hầu hết sẽ được phục vụ tốt nhất bằng cách tái sử dụng thư viện [streaming](#streaming-library) được cung cấp để xem I2P như một mạng dựa trên luồng dữ liệu.

---

### Tunnels

Cả tunnel đến và tunnel đi đều hoạt động theo các nguyên tắc tương tự. Gateway tunnel tích lũy một số lượng tunnel message, sau đó tiền xử lý chúng thành dạng phù hợp cho việc truyền tải qua tunnel. Tiếp theo, gateway mã hóa dữ liệu đã tiền xử lý đó và chuyển tiếp đến hop đầu tiên. Peer đó và các tunnel participant tiếp theo sẽ thêm một lớp mã hóa sau khi xác minh rằng đó không phải là bản sao trùng lặp trước khi chuyển tiếp đến peer tiếp theo. Cuối cùng, message đến endpoint nơi các message được tách ra một lần nữa và chuyển tiếp theo yêu cầu. Sự khác biệt nằm ở việc người tạo tunnel làm gì — đối với inbound tunnel, người tạo là endpoint và họ chỉ đơn giản giải mã tất cả các lớp đã được thêm vào, trong khi đối với outbound tunnel, người tạo là gateway và họ giải mã trước tất cả các lớp để sau khi tất cả các lớp mã hóa per-hop được thêm vào, message sẽ đến tunnel endpoint ở dạng rõ ràng.

Việc lựa chọn các peer cụ thể để chuyển tiếp tin nhắn cũng như thứ tự đặc biệt của chúng là quan trọng để hiểu cả đặc tính ẩn danh và hiệu suất của I2P. Trong khi network database (bên dưới) có tiêu chí riêng để chọn peer nào để truy vấn và lưu trữ các mục, những người tạo tunnel có thể sử dụng bất kỳ peer nào trong mạng theo bất kỳ thứ tự nào (và thậm chí với số lượng bất kỳ) trong một tunnel duy nhất. Nếu dữ liệu về độ trễ và dung lượng hoàn hảo được biết trên toàn cầu, việc lựa chọn và sắp xếp sẽ được điều khiển bởi nhu cầu cụ thể của client kết hợp với mô hình đe dọa của họ. Thật không may, dữ liệu về độ trễ và dung lượng không đơn giản để thu thập một cách ẩn danh, và việc phụ thuộc vào các peer không đáng tin cậy để cung cấp thông tin này có những hàm ý ẩn danh nghiêm trọng riêng.

Từ góc độ ẩn danh, kỹ thuật đơn giản nhất sẽ là chọn các peer ngẫu nhiên từ toàn bộ mạng lưới, sắp xếp chúng một cách ngẫu nhiên và sử dụng các peer đó theo thứ tự đó mãi mãi. Từ góc độ hiệu suất, kỹ thuật đơn giản nhất sẽ là chọn các peer nhanh nhất có đủ dung lượng dự phòng cần thiết, phân tán tải trên các peer khác nhau để xử lý failover minh bạch, và xây dựng lại tunnel bất cứ khi nào thông tin dung lượng thay đổi. Trong khi cách trước vừa dễ hỏng vừa không hiệu quả, cách sau đòi hỏi thông tin không thể truy cập được và không cung cấp đủ tính ẩn danh. Thay vào đó, I2P đang làm việc để cung cấp một loạt các chiến lược lựa chọn peer, kết hợp với mã đo lường nhận biết tính ẩn danh để tổ chức các peer theo hồ sơ của chúng.

Là nền tảng cơ bản, I2P liên tục lập hồ sơ các peer mà nó tương tác bằng cách đo lường hành vi gián tiếp của chúng — ví dụ, khi một peer phản hồi một truy vấn netDb trong 1.3 giây, độ trễ khứ hồi đó được ghi lại trong hồ sơ của tất cả các router liên quan trong hai tunnel (inbound và outbound) mà yêu cầu và phản hồi đã đi qua, cũng như hồ sơ của peer được truy vấn. Đo lường trực tiếp, chẳng hạn như độ trễ tầng transport hoặc tắc nghẽn, không được sử dụng như một phần của hồ sơ, vì nó có thể bị thao túng và liên kết với router đo lường, khiến chúng dễ bị các cuộc tấn công đơn giản. Trong khi thu thập các hồ sơ này, một loạt các phép tính được chạy trên từng hồ sơ để tổng hợp hiệu suất của nó — độ trễ, khả năng xử lý nhiều hoạt động, liệu chúng có đang bị quá tải hay không, và mức độ tích hợp tốt vào mạng. Các phép tính này sau đó được so sánh cho các peer đang hoạt động để tổ chức các router thành bốn tầng — nhanh và công suất cao, công suất cao, không bị lỗi, và đang lỗi. Các ngưỡng cho những tầng đó được xác định động, và mặc dù chúng hiện tại sử dụng các thuật toán khá đơn giản, nhưng các phương án thay thế vẫn tồn tại.

Sử dụng dữ liệu profile này, chiến lược lựa chọn peer đơn giản và hợp lý nhất là chọn ngẫu nhiên các peer từ tầng cao nhất (nhanh và dung lượng cao), và hiện tại được triển khai cho các tunnel client. Các tunnel khám phá (được sử dụng cho netDb và quản lý tunnel) chọn ngẫu nhiên các peer từ tầng "không lỗi" (bao gồm cả các router ở các tầng 'tốt hơn'), cho phép peer lấy mẫu các router rộng rãi hơn, hiệu quả tối ưu hóa việc lựa chọn peer thông qua [hill climbing](https://en.wikipedia.org/wiki/Hill_climbing) ngẫu nhiên hóa. Tuy nhiên, chỉ riêng các chiến lược này vẫn tiết lộ thông tin về các peer trong tầng cao nhất của router thông qua các cuộc tấn công predecessor và thu thập netDb. Ngược lại, tồn tại một số phương án thay thế mà, mặc dù không cân bằng tải đều như vậy, sẽ giải quyết các cuộc tấn công được thực hiện bởi các lớp đối thủ cụ thể.

Bằng cách chọn một key ngẫu nhiên và sắp xếp các peer theo khoảng cách XOR từ key đó, thông tin bị rò rỉ sẽ được giảm thiểu trong các cuộc tấn công predecessor và harvesting tùy theo tỷ lệ lỗi của peer và sự biến động của tier. Một chiến lược đơn giản khác để đối phó với các cuộc tấn công thu thập netDb là chỉ cố định (các) gateway của inbound tunnel nhưng vẫn ngẫu nhiên hóa các peer ở xa hơn trong tunnel. Để đối phó với các cuộc tấn công predecessor từ những kẻ thù mà client liên lạc, các điểm cuối của outbound tunnel cũng sẽ được giữ cố định. Việc lựa chọn peer nào để cố định tại điểm dễ bị tấn công nhất tất nhiên cần có giới hạn về thời gian, vì tất cả peer cuối cùng đều sẽ lỗi, do đó có thể được điều chỉnh phản ứng hoặc tránh chủ động để bắt chước thời gian trung bình đo được giữa các lỗi của router khác. Hai chiến lược này có thể được kết hợp, sử dụng một peer cố định ở vị trí dễ bị tấn công và sắp xếp dựa trên XOR trong chính các tunnel. Một chiến lược cứng nhắc hơn sẽ cố định chính xác các peer và thứ tự của một tunnel tiềm năng, chỉ sử dụng các peer riêng lẻ nếu tất cả chúng đồng ý tham gia theo cùng một cách mỗi lần. Điều này khác với sắp xếp dựa trên XOR ở chỗ predecessor và successor của mỗi peer luôn giống nhau, trong khi XOR chỉ đảm bảo thứ tự của chúng không thay đổi.

Như đã đề cập trước đó, I2P hiện tại (phiên bản 0.8) bao gồm chiến lược ngẫu nhiên phân tầng ở trên, với thứ tự dựa trên XOR. Thảo luận chi tiết hơn về các cơ chế liên quan đến hoạt động tunnel, quản lý và lựa chọn peer có thể được tìm thấy trong [đặc tả tunnel](/docs/specs/tunnel-implementation/).

---

### Network Database (netDb)

Như đã đề cập trước đó, netDb của I2P hoạt động để chia sẻ metadata của mạng. Điều này được mô tả chi tiết trong trang [cơ sở dữ liệu mạng](/docs/specs/common-structures/), nhưng một giải thích cơ bản có sẵn bên dưới.

Tất cả router I2P đều chứa một netDb cục bộ, nhưng không phải tất cả router đều tham gia vào DHT hoặc phản hồi các truy vấn leaseset. Những router tham gia vào DHT và phản hồi các truy vấn leaseset được gọi là 'floodfill'. Các router có thể được cấu hình thủ công thành floodfill, hoặc tự động trở thành floodfill nếu chúng có đủ khả năng và đáp ứng các tiêu chí khác cho hoạt động đáng tin cậy.

Các router I2P khác sẽ lưu trữ dữ liệu của họ và tra cứu dữ liệu bằng cách gửi các truy vấn 'store' và 'lookup' đơn giản tới các floodfill. Nếu một floodfill router nhận được truy vấn 'store', nó sẽ phát tán thông tin đến các floodfill router khác sử dụng [thuật toán Kademlia](http://en.wikipedia.org/wiki/Kademlia). Các truy vấn 'lookup' hiện tại hoạt động khác biệt để tránh một vấn đề bảo mật quan trọng. Khi thực hiện lookup, floodfill router sẽ không chuyển tiếp lookup đến các peer khác mà sẽ luôn tự trả lời (nếu nó có dữ liệu được yêu cầu).

Hai loại thông tin được lưu trữ trong cơ sở dữ liệu mạng.

- **RouterInfo** lưu trữ thông tin về một router I2P cụ thể và cách liên lạc với nó
- **LeaseSet** lưu trữ thông tin về một đích đến cụ thể (ví dụ: trang web I2P, máy chủ email...)

Tất cả thông tin này được ký bởi bên phát hành và xác minh bởi bất kỳ I2P router nào sử dụng hoặc lưu trữ thông tin đó. Ngoài ra, dữ liệu chứa thông tin thời gian để tránh lưu trữ các mục cũ và các cuộc tấn công có thể xảy ra. Đây cũng là lý do tại sao I2P tích hợp mã cần thiết để duy trì thời gian chính xác, thỉnh thoảng truy vấn một số máy chủ SNTP (mặc định là [pool.ntp.org](http://www.pool.ntp.org/) round robin) và phát hiện độ lệch thời gian giữa các router ở tầng vận chuyển.

Một số nhận xét bổ sung cũng rất quan trọng.

- **LeaseSet không được công bố và mã hóa:**
  Người ta có thể chỉ muốn những người cụ thể có thể truy cập đến một đích đến. Điều này có thể thực hiện bằng cách không công bố đích đến trong netDb. Tuy nhiên, bạn sẽ phải truyền đích đến bằng các phương tiện khác. Điều này được hỗ trợ bởi 'encrypted leaseSets'. Những leaseSet này chỉ có thể được giải mã bởi những người có quyền truy cập vào khóa giải mã.

- **Bootstrapping:**
  Bootstrapping netDb khá đơn giản. Một khi router quản lý để nhận được một routerInfo duy nhất của một peer có thể kết nối, nó có thể truy vấn router đó để lấy tham chiếu đến các router khác trong mạng. Hiện tại, một số người dùng đăng các file routerInfo của họ lên một website để cung cấp thông tin này. I2P tự động kết nối đến một trong những website này để thu thập các file routerInfo và bootstrap. I2P gọi quá trình bootstrap này là "reseeding".

- **Khả năng mở rộng tra cứu:**
  Các tra cứu trong mạng I2P là lặp lại (iterative), không phải đệ quy (recursive). Nếu tra cứu từ một floodfill thất bại, tra cứu sẽ được lặp lại với floodfill gần nhất tiếp theo. Floodfill không đệ quy hỏi floodfill khác để lấy dữ liệu. Tra cứu lặp lại có thể mở rộng cho các mạng DHT lớn.

---

### Giao thức Truyền tải

Việc giao tiếp giữa các router cần cung cấp tính bảo mật và toàn vẹn chống lại các đối thủ bên ngoài đồng thời xác thực rằng router được liên hệ là router đúng sẽ nhận một thông điệp nhất định. Các chi tiết cụ thể về cách các router giao tiếp với nhau không quan trọng — ba giao thức riêng biệt đã được sử dụng tại các thời điểm khác nhau để cung cấp những yêu cầu cơ bản đó.

I2P hiện tại hỗ trợ hai giao thức truyền tải, [NTCP2](/docs/specs/ntcp2/) qua TCP, và [SSU2](/docs/specs/ssu2/) qua UDP. Những giao thức này đã thay thế các phiên bản trước đó của các giao thức, [NTCP](/docs/legacy/ssu/) và [SSU](/docs/legacy/ssu/), hiện đã được ngừng sử dụng. Cả hai giao thức đều hỗ trợ cả IPv4 và IPv6. Bằng cách hỗ trợ cả hai phương thức truyền tải TCP và UDP, I2P có thể vượt qua hiệu quả hầu hết các tường lửa, bao gồm cả những tường lửa nhằm chặn lưu lượng trong các chế độ kiểm duyệt hạn chế. NTCP2 và SSU2 được thiết kế để sử dụng các tiêu chuẩn mã hóa hiện đại, cải thiện khả năng chống nhận diện lưu lượng, tăng hiệu quả và bảo mật, và làm cho việc vượt qua NAT mạnh mẽ hơn. Các router công bố từng phương thức truyền tải được hỗ trợ và địa chỉ IP trong cơ sở dữ liệu mạng. Các router có quyền truy cập vào mạng IPv4 và IPv6 công cộng thường sẽ công bố bốn địa chỉ, một cho mỗi kết hợp của NTCP2/SSU2 với IPv4/IPv6.

[SSU2](/docs/specs/ssu2/) hỗ trợ và mở rộng các mục tiêu của SSU. SSU2 có nhiều điểm tương đồng với các giao thức hiện đại dựa trên UDP khác như Wireguard và QUIC. Ngoài việc truyền tải đáng tin cậy các thông điệp mạng qua UDP, SSU2 còn cung cấp các tính năng chuyên biệt cho peer-to-peer, phát hiện địa chỉ IP hợp tác, phát hiện tường lửa và vượt qua NAT. Như được mô tả trong [đặc tả SSU](/docs/legacy/ssu/):

> Mục tiêu của giao thức này là cung cấp việc truyền tải thông điệp an toàn, được xác thực, bán tin cậy và không theo thứ tự, chỉ lộ ra một lượng dữ liệu tối thiểu có thể dễ dàng phân biệt được bởi các bên thứ ba. Nó nên hỗ trợ truyền thông mức độ cao cũng như kiểm soát tắc nghẽn thân thiện với TCP và có thể bao gồm phát hiện PMTU. Nó nên có khả năng di chuyển hiệu quả dữ liệu lớn với tốc độ đủ cho người dùng gia đình. Ngoài ra, nó nên hỗ trợ các kỹ thuật để giải quyết các trở ngại mạng, như hầu hết NAT hoặc tường lửa.

[NTCP2](/docs/specs/ntcp2/) hỗ trợ và mở rộng các mục tiêu của NTCP. Nó cung cấp một phương thức truyền tải hiệu quả và được mã hóa hoàn toàn cho các thông điệp mạng qua TCP, và khả năng chống nhận dạng lưu lượng, sử dụng các tiêu chuẩn mã hóa hiện đại.

I2P hỗ trợ đồng thời nhiều transport. Một transport cụ thể cho kết nối outbound được chọn bằng "bids" (đấu giá). Mỗi transport sẽ đấu giá cho kết nối và giá trị tương đối của những lần đấu giá này sẽ xác định độ ưu tiên. Các transport có thể trả lời với các mức giá khác nhau, tùy thuộc vào việc liệu đã có kết nối được thiết lập tới peer hay chưa.

Các giá trị bid (ưu tiên) phụ thuộc vào cách triển khai và có thể thay đổi dựa trên điều kiện lưu lượng, số lượng kết nối và các yếu tố khác. Các router cũng công bố tùy chọn transport của chúng cho các kết nối đến trong cơ sở dữ liệu mạng dưới dạng "chi phí" transport cho từng transport và địa chỉ.

---

### Mật mã học

I2P sử dụng mã hóa ở nhiều lớp giao thức khác nhau để mã hóa, xác thực và xác minh. Các lớp giao thức chính bao gồm: transport, tunnel build messages, tunnel layer encryption, network database messages, và end-to-end (garlic) messages. Thiết kế ban đầu của I2P sử dụng một tập hợp nhỏ các nguyên tố mã hóa vào thời điểm đó được coi là an toàn. Những nguyên tố này bao gồm mã hóa bất đối xứng ElGamal, chữ ký DSA-SHA1, mã hóa đối xứng AES256/CBC, và hash SHA-256. Khi sức mạnh tính toán có sẵn tăng lên và nghiên cứu mật mã học phát triển đáng kể qua các năm, I2P cần nâng cấp các nguyên tố và giao thức của mình. Do đó, chúng tôi đã thêm khái niệm "encryption types" (các loại mã hóa) và "signature types" (các loại chữ ký), và mở rộng các giao thức của chúng tôi để bao gồm các định danh này và chỉ ra sự hỗ trợ. Điều này cho phép chúng tôi định kỳ cập nhật và mở rộng hỗ trợ mạng lưới cho mật mã học hiện đại và đảm bảo tương lai cho mạng lưới với các nguyên tố mới, mà không phá vỡ khả năng tương thích ngược hoặc yêu cầu "flag day" cho các bản cập nhật mạng lưới. Một số signature types và encryption types cũng được dành riêng cho mục đích thử nghiệm.

Các thuật toán cơ sở hiện tại được sử dụng trong hầu hết các lớp giao thức là trao đổi khóa X25519, chữ ký EdDSA, mã hóa đối xứng có xác thực ChaCha20/Poly1305, và hàm băm SHA-256. AES256 vẫn được sử dụng cho mã hóa lớp tunnel. Những giao thức hiện đại này được sử dụng cho phần lớn giao tiếp mạng. Các thuật toán cũ bao gồm ElGamal, ECDSA, và DSA-SHA1 tiếp tục được hỗ trợ bởi hầu hết các triển khai để tương thích ngược khi giao tiếp với các router cũ hơn. Một số giao thức cũ đã bị loại bỏ và/hoặc gỡ bỏ hoàn toàn. Trong tương lai gần, chúng tôi sẽ bắt đầu nghiên cứu việc chuyển đổi sang mã hóa và chữ ký hậu lượng tử (PQ) hoặc hybrid-PQ để duy trì các tiêu chuẩn bảo mật mạnh mẽ của chúng tôi.

Các nguyên thủy mật mã này được kết hợp với nhau để cung cấp các lớp phòng thủ của I2P chống lại nhiều loại đối thủ khác nhau. Ở mức thấp nhất, giao tiếp giữa các router được bảo vệ bởi bảo mật lớp vận chuyển. Các thông điệp [tunnel](#tunnels) được truyền qua các phương thức vận chuyển có mã hóa phân lớp riêng. Nhiều thông điệp khác được truyền bên trong "garlic messages", cũng được mã hóa.

#### Garlic Messages

Garlic messages là một phần mở rộng của mã hóa phân lớp "onion", cho phép nội dung của một tin nhắn duy nhất chứa nhiều "cloves" — các tin nhắn hoàn chỉnh cùng với hướng dẫn gửi riêng của chúng. Các tin nhắn được bọc vào một garlic message bất cứ khi nào tin nhắn có thể sẽ được truyền dưới dạng văn bản rõ qua một peer không được phép truy cập vào thông tin đó — ví dụ, khi một router muốn yêu cầu router khác tham gia vào một tunnel, họ sẽ bọc yêu cầu đó bên trong một garlic, mã hóa garlic đó bằng khóa công khai của router nhận, và chuyển tiếp qua một tunnel. Một ví dụ khác là khi một client muốn gửi tin nhắn đến một đích — router của người gửi sẽ bọc tin nhắn dữ liệu đó (cùng với một số tin nhắn khác) vào một garlic, mã hóa garlic đó bằng khóa công khai được công bố trong leaseSet của người nhận, và chuyển tiếp qua các tunnel thích hợp.

Các "hướng dẫn" đính kèm với mỗi clove bên trong lớp mã hóa bao gồm khả năng yêu cầu clove được chuyển tiếp cục bộ, đến một router từ xa, hoặc đến một tunnel từ xa trên một router từ xa. Có các trường trong những hướng dẫn đó cho phép một peer yêu cầu việc giao hàng bị hoãn lại cho đến khi đạt được một thời gian hoặc điều kiện nhất định, mặc dù chúng sẽ không được thực hiện cho đến khi các [độ trễ không tầm thường](#variable-latency) được triển khai. Có thể định tuyến rõ ràng các garlic message qua bất kỳ số hop nào mà không cần xây dựng tunnel, hoặc thậm chí định tuyến lại các tunnel message bằng cách bọc chúng trong garlic message và chuyển tiếp chúng qua một số hop trước khi giao chúng đến hop tiếp theo trong tunnel, nhưng những kỹ thuật đó hiện không được sử dụng trong implementation hiện tại.

#### Thẻ Phiên

Là một hệ thống không đáng tin cậy, không có thứ tự, dựa trên thông điệp, I2P sử dụng một kết hợp đơn giản của các thuật toán mã hóa bất đối xứng và đối xứng để cung cấp tính bảo mật và toàn vẹn dữ liệu cho các garlic message. Kết hợp ban đầu được gọi là ElGamal/AES+SessionTags, nhưng đó là một cách mô tả quá dài dòng cho việc sử dụng đơn giản 2048bit ElGamal, AES256, SHA256 và nonce 32 byte. Mặc dù giao thức này vẫn được hỗ trợ, phần lớn mạng lưới đã di chuyển sang một giao thức mới, ECIES-X25519-AEAD-Ratchet. Giao thức này kết hợp X25519, ChaCha20/Poly1305, và một PRNG đồng bộ để tạo ra các nonce 32 byte. Cả hai giao thức sẽ được mô tả ngắn gọn dưới đây.

#### ElGamal/AES+SessionTags

Lần đầu tiên một router muốn mã hóa một garlic message tới router khác, chúng mã hóa tài liệu khóa cho một session key AES256 bằng ElGamal và thêm payload được mã hóa AES256/CBC sau khối ElGamal đã mã hóa đó. Ngoài payload đã mã hóa, phần được mã hóa AES còn chứa độ dài payload, mã băm SHA256 của payload chưa mã hóa, cũng như một số "session tags" — các nonce ngẫu nhiên 32 byte. Lần tiếp theo người gửi muốn mã hóa một garlic message tới router khác, thay vì mã hóa ElGamal một session key mới, họ chỉ đơn giản chọn một trong những session tags đã gửi trước đó và mã hóa AES payload như trước, sử dụng session key được dùng với session tag đó, được đặt trước bởi chính session tag đó. Khi một router nhận được một garlic encrypted message, họ kiểm tra 32 byte đầu tiên để xem có khớp với một session tag có sẵn hay không — nếu khớp, họ chỉ đơn giản giải mã AES thông điệp, nhưng nếu không khớp, họ giải mã ElGamal khối đầu tiên.

Mỗi session tag chỉ có thể được sử dụng một lần để ngăn chặn các đối thủ nội bộ tương quan không cần thiết các thông điệp khác nhau như đang truyền giữa cùng các router. Người gửi thông điệp được mã hóa ElGamal/AES+SessionTag chọn thời điểm và số lượng tag để giao, dự trữ trước cho người nhận đủ tag để bao phủ một loạt thông điệp. Garlic messages có thể phát hiện việc giao tag thành công bằng cách đóng gói một thông điệp bổ sung nhỏ như một clove ("delivery status message") — khi garlic message đến người nhận dự định và được giải mã thành công, thông điệp delivery status nhỏ này là một trong những clove được tiết lộ và có hướng dẫn cho người nhận gửi clove trở lại cho người gửi ban đầu (thông qua một inbound tunnel, tất nhiên). Khi người gửi ban đầu nhận được delivery status message này, họ biết rằng các session tag được đóng gói trong garlic message đã được giao thành công.

Bản thân các session tag có thời gian tồn tại rất ngắn, sau đó chúng sẽ bị loại bỏ nếu không được sử dụng. Ngoài ra, số lượng được lưu trữ cho mỗi khóa bị giới hạn, cũng như số lượng khóa - nếu có quá nhiều khóa đến, các thông điệp mới hoặc cũ có thể bị loại bỏ. Bên gửi theo dõi liệu các thông điệp sử dụng session tag có được truyền đi hay không, và nếu không có đủ giao tiếp thì có thể loại bỏ những thông điệp trước đó được cho là đã được giao thành công, quay trở lại sử dụng mã hóa ElGamal đầy đủ tốn kém.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags yêu cầu chi phí overhead đáng kể theo nhiều cách. Việc sử dụng CPU cao vì ElGamal khá chậm. Băng thông bị lãng phí quá mức vì phải gửi trước một lượng lớn session tag, và vì khóa công khai ElGamal rất lớn. Việc sử dụng bộ nhớ cao do yêu cầu lưu trữ một lượng lớn session tag. Độ tin cậy bị cản trở bởi việc mất mát session tag khi gửi.

ECIES-X25519-AEAD-Ratchet được thiết kế để giải quyết những vấn đề này. X25519 được sử dụng cho việc trao đổi khóa. ChaCha20/Poly1305 được sử dụng cho mã hóa đối xứng có xác thực. Khóa mã hóa được "double ratcheted" hoặc luân chuyển định kỳ. Session tags được giảm từ 32 byte xuống 8 byte và được tạo ra bằng PRNG. Giao thức này có nhiều điểm tương đồng với signal protocol được sử dụng trong Signal và WhatsApp. Giao thức này cung cấp chi phí tổng thể thấp hơn đáng kể về CPU, RAM và băng thông.

Các session tag được tạo ra từ một PRNG đồng bộ xác định chạy tại cả hai đầu của phiên để tạo session tag và session key. PRNG là một HKDF sử dụng SHA-256 HMAC, và được khởi tạo từ kết quả X25519 DH. Session tag không bao giờ được truyền trước; chúng chỉ được bao gồm cùng với thông điệp. Người nhận lưu trữ một số lượng hạn chế các session key, được lập chỉ mục theo session tag. Người gửi không cần lưu trữ bất kỳ session tag hoặc key nào vì chúng không được gửi trước; chúng có thể được tạo ra theo yêu cầu. Bằng cách giữ PRNG này đồng bộ tương đối giữa người gửi và người nhận (người nhận tính toán trước một cửa sổ của ví dụ 50 tag tiếp theo), chi phí của việc định kỳ đóng gói một số lượng lớn tag được loại bỏ.

---

## Tương lai

Các giao thức của I2P hoạt động hiệu quả trên hầu hết các nền tảng, bao gồm điện thoại di động, và bảo mật cho hầu hết các mô hình mối đe dọa. Tuy nhiên, có một số lĩnh vực cần cải thiện thêm để đáp ứng nhu cầu của những người đối mặt với các đối thủ mạnh mẽ được tài trợ bởi nhà nước, và để đối phó với các mối đe dọa từ sự tiến bộ liên tục trong mật mã học và sức mạnh máy tính ngày càng tăng. Hai tính năng có thể được thực hiện là restricted routes (tuyến đường hạn chế) và variable latency (độ trễ biến thiên) đã được jrandom đề xuất vào năm 2003. Mặc dù chúng tôi không còn dự định triển khai những tính năng này, chúng được mô tả dưới đây.

### Hoạt động Route Hạn chế

I2P là một mạng lớp phủ được thiết kế để chạy trên một mạng chuyển mạch gói đang hoạt động, khai thác nguyên tắc từ đầu đến cuối để cung cấp tính ẩn danh và bảo mật. Trong khi Internet không còn hoàn toàn tuân thủ nguyên tắc từ đầu đến cuối (do việc sử dụng NAT), I2P vẫn yêu cầu một phần đáng kể của mạng phải có thể truy cập được — có thể có một số peer dọc theo các cạnh chạy bằng các tuyến đường bị hạn chế, nhưng I2P không bao gồm thuật toán định tuyến phù hợp cho trường hợp thoái hóa khi hầu hết các peer không thể truy cập được. Tuy nhiên, nó sẽ hoạt động trên một mạng sử dụng thuật toán như vậy.

Hoạt động restricted route, nơi có giới hạn về những peer nào có thể tiếp cận trực tiếp, có một số tác động khác nhau về chức năng và tính ẩn danh, tùy thuộc vào cách các restricted route được xử lý. Ở mức độ cơ bản nhất, restricted route tồn tại khi một peer nằm sau NAT hoặc tường lửa không cho phép kết nối đến. Vấn đề này đã được giải quyết phần lớn bằng cách tích hợp distributed hole punching vào lớp transport, cho phép những người đằng sau hầu hết các NAT và tường lửa nhận được kết nối không mong muốn mà không cần cấu hình gì. Tuy nhiên, điều này không hạn chế việc lộ địa chỉ IP của peer với các router bên trong mạng, vì chúng có thể đơn giản được giới thiệu đến peer thông qua introducer đã được công bố.

Ngoài việc xử lý chức năng của các tuyến đường hạn chế, có hai cấp độ hoạt động hạn chế có thể được sử dụng để giới hạn việc tiết lộ địa chỉ IP của người dùng — sử dụng tunnel riêng của router để liên lạc, và cung cấp 'client router'. Đối với cách thức đầu tiên, các router có thể xây dựng một pool tunnel mới hoặc tái sử dụng exploratory pool của chúng, xuất bản các inbound gateway của một số tunnel như một phần của routerInfo thay vì địa chỉ transport của chúng. Khi một peer muốn liên lạc với chúng, họ sẽ thấy những tunnel gateway đó trong netDb và chỉ cần gửi thông điệp có liên quan đến chúng thông qua một trong những tunnel đã được xuất bản. Nếu peer phía sau tuyến đường hạn chế muốn trả lời, họ có thể làm như vậy trực tiếp (nếu họ sẵn sàng tiết lộ IP của mình cho peer) hoặc gián tiếp thông qua các outbound tunnel của họ. Khi các router mà peer có kết nối trực tiếp muốn tiếp cận nó (để chuyển tiếp các thông điệp tunnel chẳng hạn), chúng chỉ cần ưu tiên kết nối trực tiếp hơn tunnel gateway đã được xuất bản. Khái niệm 'client router' đơn giản là mở rộng tuyến đường hạn chế bằng cách không xuất bản bất kỳ địa chỉ router nào. Router như vậy thậm chí không cần xuất bản routerInfo của mình trong netDb, chỉ cần cung cấp routerInfo tự ký của họ cho các peer mà nó liên lạc (cần thiết để truyền các khóa công khai của router).

Có những đánh đổi cho những router đằng sau các tuyến đường bị hạn chế, vì chúng có thể sẽ ít tham gia vào tunnel của người khác hơn, và các router mà chúng kết nối tới sẽ có thể suy luận các mẫu lưu lượng mà về mặt khác sẽ không bị lộ ra. Mặt khác, nếu chi phí của việc lộ thông tin đó ít hơn chi phí của việc một IP được công khai, thì có thể điều đó là đáng giá. Tất nhiên, điều này giả định rằng các peer mà router đằng sau tuyến đường bị hạn chế liên lạc không có ý đồ xấu — hoặc mạng lưới đủ lớn để xác suất sử dụng một peer có ý đồ xấu để kết nối là đủ nhỏ, hoặc các peer đáng tin cậy (và có thể tạm thời) được sử dụng thay thế.

Restricted routes phức tạp, và mục tiêu tổng thể đã phần lớn bị bỏ rơi. Một số cải tiến liên quan đã giảm đáng kể nhu cầu đối với chúng. Chúng tôi hiện hỗ trợ UPnP để tự động mở các cổng tường lửa. Chúng tôi hỗ trợ cả IPv4 và IPv6. SSU2 đã cải thiện phát hiện địa chỉ, xác định trạng thái tường lửa và NAT hole punching hợp tác. SSU2, NTCP2, và kiểm tra tương thích địa chỉ đảm bảo rằng các tunnel hops có thể kết nối trước khi tunnel được xây dựng. GeoIP và nhận dạng quốc gia cho phép chúng tôi tránh các peer ở các quốc gia có tường lửa hạn chế. Hỗ trợ cho các router "ẩn" đằng sau những tường lửa đó đã được cải thiện. Một số triển khai cũng hỗ trợ kết nối đến các peer trên các mạng overlay như Yggdrasil.

### Độ Trễ Biến Thiên

Mặc dù phần lớn các nỗ lực ban đầu của I2P tập trung vào giao tiếp độ trễ thấp, nhưng nó được thiết kế từ đầu với mục tiêu hỗ trợ các dịch vụ độ trễ biến thiên. Ở mức cơ bản nhất, các ứng dụng chạy trên I2P có thể cung cấp tính ẩn danh của giao tiếp độ trễ trung bình và cao trong khi vẫn pha trộn các mẫu lưu lượng của chúng với lưu lượng độ trễ thấp. Tuy nhiên, về mặt nội bộ, I2P có thể cung cấp giao tiếp độ trễ trung bình và cao của riêng mình thông qua garlic encryption — chỉ định rằng tin nhắn nên được gửi sau một độ trễ nhất định, vào một thời điểm nhất định, sau khi một số lượng tin nhắn nhất định đã được truyền qua, hoặc một chiến lược mix khác. Với mã hóa phân lớp, chỉ có router mà clove tiết lộ yêu cầu trì hoãn mới biết rằng tin nhắn yêu cầu độ trễ cao, cho phép lưu lượng pha trộn sâu hơn với lưu lượng độ trễ thấp. Khi điều kiện truyền tải được đáp ứng, router nắm giữ clove (bản thân nó có thể là một tin nhắn garlic) chỉ đơn giản chuyển tiếp nó theo yêu cầu — đến một router, đến một tunnel, hoặc rất có thể, đến một điểm đến client từ xa.

Mục tiêu của các dịch vụ độ trễ thay đổi đòi hỏi tài nguyên đáng kể cho các cơ chế lưu trữ và chuyển tiếp để hỗ trợ nó. Những cơ chế này có thể và đang được hỗ trợ trong các ứng dụng nhắn tin khác nhau, chẳng hạn như i2p-bote. Ở cấp độ mạng, các mạng thay thế như Freenet cung cấp những dịch vụ này. Chúng tôi đã quyết định không theo đuổi mục tiêu này ở cấp độ I2P router.

---

## Các Hệ thống Tương tự

Kiến trúc của I2P được xây dựng dựa trên các khái niệm về middleware hướng thông điệp, cấu trúc liên kết của DHT, tính ẩn danh và mật mã học của free route mixnet, và khả năng thích ứng của mạng chuyển mạch gói. Tuy nhiên, giá trị không đến từ các khái niệm hoặc thuật toán mới lạ, mà từ việc kỹ thuật cẩn thận kết hợp các kết quả nghiên cứu từ các hệ thống và bài báo hiện có. Mặc dù có một số nỗ lực tương tự đáng để xem xét, cả về mặt so sánh kỹ thuật và chức năng, hai hệ thống đặc biệt được nhấn mạnh ở đây là Tor và Freenet.

Xem thêm [Trang So sánh Mạng](/docs/overview/comparison/). Lưu ý rằng những mô tả này được viết bởi jrandom vào năm 2003 và có thể hiện tại không còn chính xác.

### Tor

*[trang web](https://www.torproject.org/)*

Thoạt nhìn, Tor và I2P có nhiều điểm tương đồng về chức năng và tính ẩn danh. Mặc dù việc phát triển I2P bắt đầu trước khi chúng tôi biết đến những nỗ lực giai đoạn đầu của Tor, nhưng nhiều bài học từ onion routing gốc và các nỗ lực của ZKS đã được tích hợp vào thiết kế của I2P. Thay vì xây dựng một hệ thống tập trung về bản chất đáng tin cậy với các directory server, I2P có một cơ sở dữ liệu mạng tự tổ chức với mỗi peer đảm nhận trách nhiệm lập hồ sơ các router khác để xác định cách tận dụng tốt nhất các tài nguyên có sẵn. Một điểm khác biệt quan trọng khác là trong khi cả I2P và Tor đều sử dụng các đường dẫn phân lớp và có thứ tự (tunnel và circuit/stream), I2P về cơ bản là một mạng chuyển mạch gói tin, trong khi Tor về cơ bản là mạng chuyển mạch mạch, cho phép I2P định tuyến minh bạch xung quanh tắc nghẽn hoặc các lỗi mạng khác, vận hành các đường dẫn dự phòng, và cân bằng tải dữ liệu trên các tài nguyên có sẵn. Trong khi Tor cung cấp chức năng outproxy hữu ích bằng cách tích hợp khám phá và lựa chọn outproxy, I2P để các quyết định lớp ứng dụng như vậy cho các ứng dụng chạy trên I2P — thực tế, I2P thậm chí đã đưa chính thư viện streaming giống TCP ra lớp ứng dụng, cho phép các nhà phát triển thử nghiệm với các chiến lược khác nhau, khai thác kiến thức chuyên môn của họ để cung cấp hiệu suất tốt hơn.

Từ góc độ ẩn danh, có nhiều điểm tương đồng khi so sánh các mạng lõi. Tuy nhiên, có một số khác biệt chính. Khi đối phó với kẻ thù nội bộ hoặc hầu hết các kẻ thù bên ngoài, các tunnel đơn hướng của I2P chỉ để lộ một nửa lượng dữ liệu lưu lượng so với các circuit song công của Tor bằng cách đơn giản chỉ nhìn vào các luồng dữ liệu - một yêu cầu HTTP và phản hồi sẽ đi theo cùng một đường dẫn trong Tor, trong khi ở I2P các gói tin tạo nên yêu cầu sẽ đi ra thông qua một hoặc nhiều tunnel gửi đi và các gói tin tạo nên phản hồi sẽ trở về thông qua một hoặc nhiều tunnel nhận khác. Trong khi các chiến lược lựa chọn và sắp xếp peer của I2P đủ để giải quyết các cuộc tấn công tiền nhiệm, nếu cần chuyển sang tunnel hai chiều, chúng ta có thể đơn giản xây dựng một tunnel nhận và gửi đi dọc theo các router giống nhau.

Một vấn đề ẩn danh khác xuất hiện trong việc Tor sử dụng tạo tunnel kiểu kính thiên văn, vì việc đếm gói tin đơn giản và đo lường thời gian khi các cell trong mạch đi qua node của đối thủ sẽ tiết lộ thông tin thống kê về vị trí của đối thủ trong mạch. I2P tạo tunnel đơn hướng với một thông điệp duy nhất để dữ liệu này không bị tiết lộ. Việc bảo vệ vị trí trong tunnel rất quan trọng, vì nếu không, đối thủ sẽ có thể thực hiện một loạt các cuộc tấn công predecessor, intersection và xác nhận lưu lượng mạnh mẽ.

Nhìn chung, Tor và I2P bổ sung cho nhau trong trọng tâm của chúng — Tor hướng tới việc cung cấp outproxy Internet ẩn danh tốc độ cao, trong khi I2P hướng tới việc cung cấp một mạng lưới phi tập trung có khả năng phục hồi. Về mặt lý thuyết, cả hai đều có thể được sử dụng để đạt được cả hai mục đích, nhưng với nguồn lực phát triển hạn chế, chúng đều có điểm mạnh và điểm yếu riêng. Các nhà phát triển I2P đã xem xét các bước cần thiết để sửa đổi Tor nhằm tận dụng thiết kế của I2P, nhưng lo ngại về khả năng tồn tại của Tor trong điều kiện khan hiếm tài nguyên cho thấy rằng kiến trúc chuyển mạch gói của I2P sẽ có thể khai thác các tài nguyên khan hiếm hiệu quả hơn.

### Freenet

*[trang web](http://www.freenetproject.org/)*

Freenet đóng vai trò quan trọng trong các giai đoạn ban đầu của thiết kế I2P — chứng minh tính khả thi của một cộng đồng ẩn danh sôi động hoàn toàn tồn tại trong mạng, minh chứng rằng có thể tránh được những nguy hiểm vốn có trong các outproxy. Hạt giống đầu tiên của I2P bắt đầu như một lớp giao tiếp thay thế cho Freenet, cố gắng tách biệt những phức tạp của giao tiếp điểm-tới-điểm có thể mở rộng, ẩn danh và bảo mật khỏi những phức tạp của kho dữ liệu phân tán chống kiểm duyệt. Tuy nhiên, theo thời gian, một số vấn đề về tính ẩn danh và khả năng mở rộng vốn có trong các thuật toán của Freenet đã làm rõ rằng I2P nên tập trung nghiêm túc vào việc cung cấp một lớp giao tiếp ẩn danh tổng quát, thay vì là một thành phần của Freenet. Qua nhiều năm, các nhà phát triển Freenet đã nhận ra những điểm yếu trong thiết kế cũ, khiến họ đề xuất rằng họ sẽ cần một lớp "premix" để cung cấp tính ẩn danh đáng kể. Nói cách khác, Freenet cần chạy trên một mixnet như I2P hoặc Tor, với các "client node" yêu cầu và xuất bản dữ liệu thông qua mixnet đến các "server node" sau đó tìm nạp và lưu trữ dữ liệu theo các thuật toán lưu trữ dữ liệu phân tán theo phương pháp heuristic của Freenet.

Chức năng của Freenet rất bổ sung cho I2P, vì Freenet tự nhiên cung cấp nhiều công cụ để vận hành các hệ thống có độ trễ trung bình và cao, trong khi I2P tự nhiên cung cấp mạng trộn độ trễ thấp phù hợp để cung cấp tính ẩn danh đầy đủ. Logic tách mixnet khỏi kho dữ liệu phân tán chống kiểm duyệt vẫn có vẻ hiển nhiên từ góc độ kỹ thuật, tính ẩn danh, bảo mật và phân bổ tài nguyên, vì vậy hy vọng đội ngũ Freenet sẽ theo đuổi các nỗ lực theo hướng đó, nếu không chỉ đơn giản là tái sử dụng (hoặc giúp cải thiện, khi cần thiết) các mixnet hiện có như I2P hoặc Tor.

---

## Phụ lục A: Tầng Ứng dụng

I2P bản thân không thực sự làm nhiều việc — nó chỉ đơn giản gửi tin nhắn đến các đích từ xa và nhận tin nhắn nhắm đến các đích cục bộ — hầu hết công việc thú vị diễn ra ở các lớp phía trên nó. Xét riêng, I2P có thể được coi như một lớp IP ẩn danh và bảo mật, và [thư viện streaming](#streaming-library) đi kèm như một triển khai của lớp TCP ẩn danh và bảo mật trên đó. Ngoài ra, [I2PTunnel](#i2ptunnel) cung cấp một hệ thống proxy TCP tổng quát để kết nối vào hoặc ra khỏi mạng I2P, cùng với nhiều ứng dụng mạng khác nhau cung cấp thêm chức năng cho người dùng cuối.

### Thư viện Streaming

Thư viện streaming I2P có thể được xem như một giao diện streaming tổng quát (tương tự TCP sockets), và việc triển khai hỗ trợ [sliding window protocol](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) với một số tối ưu hóa, để tính đến độ trễ cao trên I2P. Các stream riêng lẻ có thể điều chỉnh kích thước gói tin tối đa và các tùy chọn khác, mặc dù mặc định là 4KB nén có vẻ là sự cân bằng hợp lý giữa chi phí băng thông của việc truyền lại các thông điệp bị mất và độ trễ của nhiều thông điệp.

Ngoài ra, xét đến chi phí tương đối cao của các thông điệp tiếp theo, giao thức của thư viện streaming để lập lịch và chuyển phát thông điệp đã được tối ưu hóa để cho phép các thông điệp riêng lẻ được truyền chứa càng nhiều thông tin có sẵn càng tốt. Ví dụ, một giao dịch HTTP nhỏ được ủy quyền thông qua thư viện streaming có thể hoàn thành trong một lượt truyền duy nhất — thông điệp đầu tiên gộp chung SYN, FIN và payload nhỏ (một HTTP request thường vừa đủ) và phản hồi gộp chung SYN, FIN, ACK và payload nhỏ (nhiều HTTP response vừa đủ). Mặc dù một ACK bổ sung phải được truyền để báo cho HTTP server biết rằng SYN/FIN/ACK đã được nhận, nhưng HTTP proxy cục bộ có thể chuyển phản hồi đầy đủ cho trình duyệt ngay lập tức.

Tuy nhiên, nhìn chung, thư viện streaming có nhiều điểm tương đồng với sự trừu tượng hóa của TCP, với các cửa sổ trượt, thuật toán kiểm soát tắc nghẽn (cả slow start và tránh tắc nghẽn), và hành vi gói tin chung (ACK, SYN, FIN, RST, v.v.).

### Thư viện Đặt tên và Sổ địa chỉ

*Để biết thêm thông tin, xem trang [Đặt tên và Sổ địa chỉ](/docs/overview/naming/).*

*Được phát triển bởi: mihi, Ragnarok*

Đặt tên trong I2P đã là một chủ đề được tranh luận nhiều ngay từ những ngày đầu với những người ủng hộ trên khắp phổ khả năng. Tuy nhiên, với nhu cầu vốn có của I2P về giao tiếp an toàn và hoạt động phi tập trung, hệ thống đặt tên kiểu DNS truyền thống rõ ràng bị loại bỏ, cũng như các hệ thống bỏ phiếu "đa số quyết định". Thay vào đó, I2P đi kèm với một thư viện đặt tên tổng quát và một triển khai cơ bản được thiết kế để hoạt động dựa trên ánh xạ tên địa phương tới destination, cũng như một ứng dụng bổ sung tùy chọn gọi là "Address Book". Address book là một hệ thống đặt tên an toàn, phân tán và có thể đọc được bằng ngôn ngữ tự nhiên, được điều khiển bởi web-of-trust, chỉ hy sinh yêu cầu tất cả tên có thể đọc được phải duy nhất trên toàn cầu bằng cách chỉ yêu cầu tính duy nhất cục bộ. Trong khi tất cả thông điệp trong I2P được định địa chỉ bằng mật mã qua destination của chúng, những người khác nhau có thể có các mục address book cục bộ cho "Alice" tham chiếu đến các destination khác nhau. Mọi người vẫn có thể khám phá tên mới bằng cách nhập các address book được xuất bản của các đồng nghiệp được chỉ định trong web of trust của họ, bằng cách thêm vào các mục được cung cấp thông qua bên thứ ba, hoặc (nếu một số người tổ chức một loạt address book được xuất bản sử dụng hệ thống đăng ký ai đến trước được phục vụ trước) mọi người có thể chọn xử lý các address book này như các name server, mô phỏng DNS truyền thống.

Tuy nhiên, I2P không khuyến khích việc sử dụng các dịch vụ giống DNS, vì thiệt hại do việc tấn công chiếm quyền điều khiển một trang web có thể rất lớn — và các destination không an toàn thì không có giá trị gì. Bản thân DNSsec vẫn phải dựa vào các nhà đăng ký tên miền và cơ quan chứng nhận, trong khi với I2P, các yêu cầu gửi đến một destination không thể bị chặn bắt hoặc phản hồi bị giả mạo, vì chúng được mã hóa bằng khóa công khai của destination, và một destination chỉ đơn giản là một cặp khóa công khai và một chứng chỉ. Mặt khác, các hệ thống kiểu DNS cho phép bất kỳ name server nào trên đường dẫn tra cứu có thể thực hiện các cuộc tấn công từ chối dịch vụ đơn giản và tấn công giả mạo. Việc thêm vào một chứng chỉ xác thực các phản hồi được ký bởi một số cơ quan chứng nhận tập trung sẽ giải quyết được nhiều vấn đề của nameserver thù địch nhưng vẫn để lại lỗ hổng cho các cuộc tấn công replay cũng như các cuộc tấn công từ cơ quan chứng nhận thù địch.

Việc đặt tên theo kiểu bỏ phiếu cũng rất nguy hiểm, đặc biệt là do tính hiệu quả của các cuộc tấn công Sybil trong các hệ thống ẩn danh — kẻ tấn công có thể đơn giản tạo ra một số lượng tùy ý lớn các peer và "bỏ phiếu" bằng từng peer để chiếm quyền kiểm soát một tên nhất định. Các phương pháp proof-of-work có thể được sử dụng để làm cho việc tạo danh tính không miễn phí, nhưng khi mạng lưới phát triển thì tải cần thiết để liên lạc với mọi người để tiến hành bỏ phiếu trực tuyến là không khả thi, hoặc nếu toàn bộ mạng lưới không được truy vấn, các tập kết quả khác nhau có thể được tiếp cận.

Tuy nhiên, giống như Internet, I2P đang giữ việc thiết kế và vận hành hệ thống đặt tên tách biệt khỏi lớp truyền thông (giống IP). Thư viện đặt tên được tích hợp sẵn bao gồm một giao diện nhà cung cấp dịch vụ đơn giản mà các hệ thống đặt tên thay thế có thể cắm vào, cho phép người dùng cuối quyết định loại đánh đổi đặt tên nào họ muốn.

### I2PTunnel

*Được phát triển bởi: mihi*

I2PTunnel có lẽ là ứng dụng client phổ biến và linh hoạt nhất của I2P, cho phép proxy tổng quát cả vào và ra khỏi mạng I2P. I2PTunnel có thể được xem như bốn ứng dụng proxy riêng biệt — một "client" nhận các kết nối TCP đến và chuyển tiếp chúng đến một đích I2P nhất định, một "httpclient" (còn gọi là "eepproxy") hoạt động như một HTTP proxy và chuyển tiếp các yêu cầu đến đích I2P thích hợp (sau khi truy vấn dịch vụ đặt tên nếu cần thiết), một "server" nhận các kết nối I2P streaming đến trên một đích và chuyển tiếp chúng đến một TCP host+port nhất định, và một "httpserver" mở rộng "server" bằng cách phân tích các yêu cầu và phản hồi HTTP để cho phép hoạt động an toàn hơn. Có thêm một ứng dụng "socksclient", nhưng việc sử dụng nó không được khuyến khích vì những lý do đã đề cập trước đó.

Bản thân I2P không phải là một mạng outproxy — các lo ngại về tính ẩn danh và bảo mật vốn có trong một mix net chuyển tiếp dữ liệu vào và ra khỏi mix đã khiến thiết kế của I2P tập trung vào việc cung cấp một mạng ẩn danh có khả năng đáp ứng nhu cầu của người dùng mà không cần đến tài nguyên bên ngoài. Tuy nhiên, ứng dụng I2PTunnel "httpclient" cung cấp một hook (móc nối) cho việc outproxy — nếu hostname được yêu cầu không kết thúc bằng ".i2p", nó sẽ chọn ngẫu nhiên một destination từ tập hợp outproxy do người dùng cung cấp và chuyển tiếp yêu cầu đến chúng. Những destination này đơn giản chỉ là các instance I2PTunnel "server" được vận hành bởi những tình nguyện viên đã chủ động lựa chọn chạy outproxy — không ai là outproxy theo mặc định, và việc chạy outproxy không tự động thông báo cho người khác proxy qua bạn. Mặc dù outproxy có những điểm yếu vốn có, chúng cung cấp một proof of concept đơn giản cho việc sử dụng I2P và mang lại một số chức năng dưới mô hình đe dọa có thể đủ cho một số người dùng.

I2PTunnel cho phép hầu hết các ứng dụng hoạt động. Một "httpserver" trỏ đến máy chủ web cho phép bất kỳ ai vận hành trang web ẩn danh của riêng họ (hay "I2P Site") — một máy chủ web được tích hợp sẵn với I2P cho mục đích này, nhưng có thể sử dụng bất kỳ máy chủ web nào. Bất kỳ ai cũng có thể chạy "client" trỏ đến một trong các máy chủ IRC được lưu trữ ẩn danh, mỗi máy chủ đang chạy "server" trỏ đến IRCd cục bộ của họ và giao tiếp giữa các IRCd qua tunnel "client" riêng của chúng. Người dùng cuối cũng có tunnel "client" trỏ đến các đích POP3 và SMTP của [I2Pmail](#i2pmail--susimail) (đây đơn giản chỉ là các instance "server" trỏ đến máy chủ POP3 và SMTP), cũng như tunnel "client" trỏ đến máy chủ CVS của I2P, cho phép phát triển ẩn danh. Đôi khi mọi người thậm chí còn chạy proxy "client" để truy cập các instance "server" trỏ đến máy chủ NNTP.

### I2PSnark

*I2PSnark được phát triển bởi: jrandom, và những người khác, được chuyển đổi từ client [Snark](http://www.klomp.org/snark/) của [mjw](http://www.klomp.org/mark/)*

Được tích hợp sẵn với bộ cài đặt I2P, I2PSnark cung cấp một BitTorrent client ẩn danh đơn giản với khả năng đa torrent, hiển thị tất cả các chức năng thông qua giao diện web HTML thuần túy.

### I2Pmail / Susimail

*Được phát triển bởi: postman, susi23, mastiejaner*

I2Pmail là một dịch vụ hơn là một ứng dụng — postman cung cấp cả email nội bộ và bên ngoài với dịch vụ POP3 và SMTP thông qua các instance I2PTunnel truy cập một loạt các thành phần được phát triển cùng với mastiejaner, cho phép mọi người sử dụng các ứng dụng mail ưa thích của họ để gửi và nhận mail một cách ẩn danh. Tuy nhiên, vì hầu hết các ứng dụng mail đều tiết lộ thông tin nhận dạng đáng kể, I2P tích hợp ứng dụng susimail dựa trên web của susi23 được xây dựng đặc biệt với tâm trí hướng đến nhu cầu ẩn danh của I2P. Dịch vụ I2Pmail/mail.i2p cung cấp lọc virus minh bạch cũng như ngăn chặn tấn công từ chối dịch vụ với các hạn ngạch được tăng cường bằng hashcash. Ngoài ra, mỗi người dùng có quyền kiểm soát chiến lược phân lô của họ trước khi giao hàng thông qua các outproxy mail.i2p, được tách biệt khỏi các máy chủ SMTP và POP3 mail.i2p — cả outproxy và inproxy đều giao tiếp với các máy chủ SMTP và POP3 mail.i2p thông qua chính I2P, vì vậy việc xâm phạm những vị trí không ẩn danh đó không cung cấp quyền truy cập vào các tài khoản mail hoặc mẫu hoạt động của người dùng.
