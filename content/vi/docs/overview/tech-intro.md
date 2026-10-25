---
title: "I2P: Giới thiệu Kỹ thuật"
description: "Giới thiệu kỹ thuật về kiến trúc và hoạt động của I2P"
slug: "tech-intro"
aliases:
  - "/vi/techintro"
  - "/vi/techintro/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

LƯU Ý: Tài liệu này ban đầu được viết bởi jrandom vào năm 2003. Mặc dù chúng tôi cố gắng cập nhật nội dung, một số thông tin có thể đã lỗi thời hoặc không đầy đủ. Các phần transport và mã hóa đã được cập nhật tính đến tháng 01-2025.

## Giới thiệu

I2P là một lớp mạng ẩn danh chuyển mạch gói có khả năng mở rộng, tự tổ chức và có tính bền vững, trên đó có thể vận hành bất kỳ số lượng ứng dụng nào quan tâm đến tính ẩn danh hoặc bảo mật. Mỗi ứng dụng này có thể tự đưa ra những đánh đổi riêng về tính ẩn danh, độ trễ và thông lượng mà không cần lo lắng về việc triển khai đúng đắn một mixnet tuyến đường tự do, cho phép chúng hòa trộn hoạt động của mình với tập hợp ẩn danh lớn hơn của những người dùng đã đang chạy trên I2P.

Các ứng dụng hiện có đã cung cấp đầy đủ các hoạt động Internet thông thường — duyệt web **ẩn danh**, lưu trữ web, trò chuyện, chia sẻ tập tin, email, viết blog và phân phối nội dung, cũng như một số ứng dụng khác đang được phát triển.

- Duyệt web: sử dụng bất kỳ trình duyệt nào hỗ trợ proxy.
- Trò chuyện: IRC và các giao thức khác
- Chia sẻ tập tin: [I2PSnark](#i2psnark) và các ứng dụng khác
- E-mail: [susimail](#i2pmail--susimail) và các ứng dụng khác
- Blog: sử dụng bất kỳ máy chủ web cục bộ nào, hoặc các plugin có sẵn

Khác với các trang web được lưu trữ trong các mạng phân phối nội dung như [Freenet](#freenet) hoặc [GNUnet](https://www.gnunet.org/en/), các dịch vụ được lưu trữ trên I2P hoàn toàn tương tác — có các công cụ tìm kiếm kiểu web truyền thống, bảng tin, blog mà bạn có thể bình luận, các trang web được điều khiển bằng cơ sở dữ liệu, và các cầu nối để truy vấn các hệ thống tĩnh như Freenet mà không cần cài đặt cục bộ.

Với tất cả các ứng dụng hỗ trợ ẩn danh này, I2P đóng vai trò là middleware hướng thông điệp — các ứng dụng báo rằng chúng muốn gửi một số dữ liệu đến một định danh mật mã (một "destination") và I2P đảm nhiệm việc đảm bảo dữ liệu đó được truyền đến một cách an toàn và ẩn danh. I2P cũng tích hợp một thư viện [streaming](#streaming-library) đơn giản để cho phép các thông điệp cố gắng tối đa ẩn danh của I2P được truyền như các luồng đáng tin cậy, theo thứ tự, minh bạch cung cấp thuật toán kiểm soát tắc nghẽn dựa trên TCP được điều chỉnh cho sản phẩm trễ băng thông cao của mạng. Mặc dù đã có một số SOCKS proxy đơn giản có sẵn để kết nối các ứng dụng hiện có vào mạng, giá trị của chúng bị hạn chế vì gần như mọi ứng dụng đều thường xuyên tiết lộ những gì, trong bối cảnh ẩn danh, là thông tin nhạy cảm. Cách duy nhất an toàn là kiểm toán đầy đủ một ứng dụng để đảm bảo hoạt động đúng đắn và để hỗ trợ điều đó, chúng tôi cung cấp một loạt API bằng nhiều ngôn ngữ khác nhau có thể được sử dụng để tận dụng tối đa mạng.

I2P không phải là một dự án nghiên cứu — học thuật, thương mại, hay chính phủ — mà thay vào đó là một nỗ lực kỹ thuật nhằm làm bất cứ điều gì cần thiết để cung cấp mức độ ẩn danh đủ cho những ai cần nó. Nó đã được phát triển tích cực từ đầu năm 2003 với một nhà phát triển toàn thời gian và một nhóm cộng tác viên bán thời gian tận tâm từ khắp nơi trên thế giới. Tất cả công việc được thực hiện trên I2P đều là mã nguồn mở và có sẵn miễn phí trên [trang web](/), với phần lớn mã được phát hành thẳng vào phạm vi công cộng, mặc dù sử dụng một vài thủ tục mã hóa theo giấy phép kiểu BSD. Những người làm việc trên I2P không kiểm soát việc mọi người phát hành các ứng dụng khách dưới giấy phép gì, và có một số ứng dụng GPL có sẵn ([I2PTunnel](#i2ptunnel), [susimail](#i2pmail--susimail), [I2PSnark](#i2psnark), I2P-Bote, I2Phex và các ứng dụng khác). Tài trợ cho I2P hoàn toàn đến từ các khoản quyên góp, và không nhận được bất kỳ miễn thuế nào ở bất kỳ khu vực tài phán nào vào thời điểm này, vì nhiều nhà phát triển bản thân họ là ẩn danh.

---

## Hoạt động

### Tổng quan

Để hiểu hoạt động của I2P, điều cần thiết là phải hiểu một số khái niệm chính. Đầu tiên, I2P tách biệt nghiêm ngặt giữa phần mềm tham gia mạng lưới (một "router") và các điểm cuối ẩn danh ("destinations") được liên kết với từng ứng dụng riêng lệ. Việc ai đó đang chạy I2P thường không phải là bí mật. Điều được ẩn giấu là thông tin về những gì người dùng đang làm, nếu có, cũng như router nào mà một destination cụ thể được kết nối tới. Người dùng cuối thường sẽ có nhiều destinations cục bộ trên router của họ — ví dụ, một destination proxy vào các máy chủ IRC, một destination khác hỗ trợ máy chủ web ẩn danh của người dùng ("I2P Site"), một destination khác cho phiên bản I2Phex, một destination khác cho torrents, v.v.

Một khái niệm quan trọng khác cần hiểu là "tunnel". Một tunnel là một đường dẫn có hướng đi qua một danh sách các router được chọn một cách rõ ràng. Mã hóa phân lớp được sử dụng, do đó mỗi router chỉ có thể giải mã một lớp duy nhất. Thông tin được giải mã chứa IP của router tiếp theo, cùng với thông tin được mã hóa cần được chuyển tiếp. Mỗi tunnel có một điểm bắt đầu (router đầu tiên, còn được gọi là "gateway") và một điểm kết thúc. Tin nhắn chỉ có thể được gửi theo một chiều. Để gửi tin nhắn trở lại, cần có một tunnel khác.

![Sơ đồ tunnel đến và tunnel đi](/images/tunnels.png) *Hình 1: Có hai loại tunnel: tunnel đến và tunnel đi.*

Có hai loại tunnel tồn tại: **"outbound tunnels"** gửi tin nhắn đi khỏi người tạo tunnel, trong khi **"inbound tunnels"** mang tin nhắn đến cho người tạo tunnel. Việc kết hợp hai loại tunnel này cho phép người dùng gửi tin nhắn cho nhau. Người gửi ("Alice" trong hình trên) thiết lập một outbound tunnel, trong khi người nhận ("Bob" trong hình trên) tạo một inbound tunnel. Gateway của một inbound tunnel có thể nhận tin nhắn từ bất kỳ người dùng nào khác và sẽ chuyển tiếp chúng cho đến endpoint ("Bob"). Endpoint của outbound tunnel sẽ cần gửi tin nhắn đến gateway của inbound tunnel. Để làm điều này, người gửi ("Alice") thêm hướng dẫn vào tin nhắn đã mã hóa của mình. Một khi endpoint của outbound tunnel giải mã tin nhắn, nó sẽ có hướng dẫn để chuyển tiếp tin nhắn đến đúng inbound gateway (gateway đến "Bob").

Khái niệm quan trọng thứ ba cần hiểu là **"network database"** (hoặc "netDb") của I2P — một cặp thuật toán được sử dụng để chia sẻ siêu dữ liệu mạng. Hai loại siêu dữ liệu được mang theo là **"routerInfo"** và **"leaseSet"** — routerInfo cung cấp cho các router dữ liệu cần thiết để liên hệ với một router cụ thể (khóa công khai, địa chỉ truyền tải, v.v.), trong khi leaseSet cung cấp cho các router thông tin cần thiết để liên hệ với một điểm đích cụ thể. Một leaseSet chứa một số "lease". Mỗi lease này chỉ định một tunnel gateway, cho phép tiếp cận một điểm đích cụ thể. Thông tin đầy đủ được chứa trong một lease:

- Inbound gateway cho một tunnel cho phép đến được một đích cụ thể.
- Thời gian khi một tunnel hết hạn.
- Cặp khóa công khai để có thể mã hóa tin nhắn (để gửi qua tunnel và đến được đích).

Các router tự gửi routerInfo của chúng trực tiếp đến netDb, trong khi các leaseSet được gửi thông qua các tunnel đầu ra (các leaseSet cần được gửi một cách ẩn danh để tránh việc liên kết một router với các leaseSet của nó).

Chúng ta có thể kết hợp các khái niệm trên để xây dựng các kết nối thành công trong mạng.

Để xây dựng các tunnel đến và đi của riêng mình, Alice thực hiện tra cứu trong netDb để thu thập routerInfo. Bằng cách này, cô ấy thu thập danh sách các peer mà cô có thể sử dụng làm hop trong các tunnel của mình. Sau đó cô có thể gửi tin nhắn xây dựng đến hop đầu tiên, yêu cầu xây dựng một tunnel và yêu cầu router đó gửi tin nhắn xây dựng tiếp tục, cho đến khi tunnel được xây dựng hoàn tất.

![Yêu cầu thông tin về các router khác](/images/netdb_get_routerinfo_1.png)

![Build tunnel using router information](/images/netdb_get_routerinfo_2.png) *Hình 2: Thông tin router được sử dụng để xây dựng tunnel.*

Khi Alice muốn gửi tin nhắn cho Bob, đầu tiên cô ấy thực hiện tra cứu trong netDb để tìm leaseSet của Bob, cung cấp cho cô ấy các gateway tunnel đầu vào hiện tại của anh ấy. Sau đó cô ấy chọn một trong các tunnel đầu ra của mình và gửi tin nhắn xuống đó với hướng dẫn cho endpoint của tunnel đầu ra chuyển tiếp tin nhắn đến một trong các gateway tunnel đầu vào của Bob. Khi endpoint tunnel đầu ra nhận được những hướng dẫn đó, nó chuyển tiếp tin nhắn theo yêu cầu, và khi gateway tunnel đầu vào của Bob nhận được nó, tin nhắn được chuyển tiếp xuống tunnel đến router của Bob. Nếu Alice muốn Bob có thể trả lời tin nhắn, cô ấy cần truyền đích đến của chính mình một cách rõ ràng như một phần của chính tin nhắn đó. Điều này có thể được thực hiện bằng cách giới thiệu một lớp cao hơn, được thực hiện trong thư viện [streaming](#streaming-library). Alice cũng có thể rút ngắn thời gian phản hồi bằng cách gói LeaseSet gần đây nhất của cô ấy cùng với tin nhắn để Bob không cần thực hiện tra cứu netDb khi anh ấy muốn trả lời, nhưng điều này là tùy chọn.

![Connect tunnels using LeaseSets](/images/netdb_get_leaseset.png) *Hình 3: LeaseSets được sử dụng để kết nối các tunnel đi và tunnel đến.*

Trong khi bản thân các tunnel đã có mã hóa nhiều lớp để ngăn chặn việc tiết lộ trái phép cho các peer bên trong mạng (như chính lớp transport cũng làm để ngăn chặn việc tiết lộ trái phép cho các peer bên ngoài mạng), cần thiết phải thêm một lớp mã hóa đầu cuối bổ sung để ẩn thông điệp khỏi điểm cuối tunnel outbound và gateway tunnel inbound. "[Garlic encryption](#garlic-messages)" này cho phép router của Alice gói nhiều thông điệp thành một "garlic message" duy nhất, được mã hóa bằng một public key cụ thể để các peer trung gian không thể xác định được có bao nhiêu thông điệp trong garlic, những thông điệp đó nói gì, hoặc các clove riêng lẻ đó được gửi đến đâu. Đối với giao tiếp đầu cuối điển hình giữa Alice và Bob, garlic sẽ được mã hóa bằng public key được công bố trong leaseSet của Bob, cho phép thông điệp được mã hóa mà không cần tiết lộ public key cho router của chính Bob.

Một sự kiện quan trọng khác cần ghi nhớ là I2P hoàn toàn dựa trên thông điệp và một số thông điệp có thể bị mất trên đường truyền. Các ứng dụng sử dụng I2P có thể sử dụng các giao diện hướng thông điệp và tự lo liệu việc kiểm soát tắc nghẽn cũng như các nhu cầu về độ tin cậy, nhưng hầu hết sẽ được phục vụ tốt nhất bằng cách tái sử dụng thư viện [streaming](#streaming-library) được cung cấp để xem I2P như một mạng dựa trên luồng dữ liệu.

---

### Tunnels

Cả tunnel đầu vào và đầu ra đều hoạt động theo các nguyên lý tương tự. Gateway tunnel tích lũy một số tunnel message, cuối cùng xử lý trước chúng thành thứ gì đó để chuyển giao tunnel. Tiếp theo, gateway mã hóa dữ liệu đã được xử lý trước đó và chuyển tiếp đến hop đầu tiên. Peer đó và các thành viên tunnel tiếp theo thêm một lớp mã hóa sau khi xác minh rằng nó không phải là bản sao trùng lặp trước khi chuyển tiếp đến peer tiếp theo. Cuối cùng, message đến endpoint nơi các message được tách ra lại và chuyển tiếp theo yêu cầu. Sự khác biệt nảy sinh trong việc người tạo tunnel làm gì — đối với tunnel đầu vào, người tạo là endpoint và họ chỉ đơn giản giải mã tất cả các lớp được thêm vào, trong khi đối với tunnel đầu ra, người tạo là gateway và họ giải mã trước tất cả các lớp để sau khi tất cả các lớp mã hóa theo từng hop được thêm vào, message đến endpoint ở dạng rõ ràng.

Việc lựa chọn các peer cụ thể để chuyển tiếp tin nhắn cũng như thứ tự sắp xếp đặc biệt của chúng rất quan trọng để hiểu cả đặc điểm ẩn danh và hiệu năng của I2P. Trong khi network database (netDb) (bên dưới) có tiêu chí riêng để chọn peer nào sẽ truy vấn và lưu trữ mục tin, những người tạo tunnel có thể sử dụng bất kỳ peer nào trong mạng theo bất kỳ thứ tự nào (và thậm chí bao nhiêu lần tùy ý) trong một tunnel duy nhất. Nếu dữ liệu độ trễ và dung lượng hoàn hảo được biết toàn cầu, việc lựa chọn và sắp xếp sẽ được điều khiển bởi nhu cầu cụ thể của client kết hợp với mô hình mối đe dọa của họ. Thật không may, dữ liệu độ trễ và dung lượng không dễ dàng thu thập một cách ẩn danh, và việc phụ thuộc vào các peer không đáng tin cậy để cung cấp thông tin này có những tác động ẩn danh nghiêm trọng riêng.

Từ góc độ ẩn danh, kỹ thuật đơn giản nhất sẽ là chọn peers ngẫu nhiên từ toàn bộ mạng, sắp xếp chúng ngẫu nhiên và sử dụng những peers đó theo thứ tự đó mãi mãi. Từ góc độ hiệu suất, kỹ thuật đơn giản nhất sẽ là chọn những peers nhanh nhất với khả năng dự phòng cần thiết, phân bổ tải trên các peers khác nhau để xử lý failover trong suốt, và xây dựng lại tunnel bất cứ khi nào thông tin khả năng thay đổi. Trong khi cách tiếp cận đầu tiên vừa mong manh vừa không hiệu quả, cách sau yêu cầu thông tin không thể truy cập được và cung cấp khả năng ẩn danh không đủ. Thay vào đó, I2P đang làm việc để cung cấp một loạt các chiến lược lựa chọn peer, kết hợp với mã đo lường nhận biết tính ẩn danh để sắp xếp các peers theo hồ sơ của chúng.

Về cơ bản, I2P liên tục lập hồ sơ cho các peer mà nó tương tác bằng cách đo lường hành vi gián tiếp của chúng — ví dụ, khi một peer phản hồi một truy vấn netDb trong 1.3 giây, độ trễ khứ hồi đó được ghi lại trong hồ sơ của tất cả các router tham gia vào hai tunnel (inbound và outbound) mà qua đó yêu cầu và phản hồi đã đi qua, cũng như hồ sơ của peer được truy vấn. Đo lường trực tiếp, chẳng hạn như độ trễ tầng transport hoặc tình trạng tắc nghẽn, không được sử dụng như một phần của hồ sơ, vì nó có thể bị thao túng và liên kết với router đang đo, khiến chúng phải đối mặt với các cuộc tấn công tầm thường. Trong khi thu thập những hồ sơ này, một loạt các phép tính được chạy trên mỗi hồ sơ để tóm tắt hiệu suất của nó — độ trễ, khả năng xử lý nhiều hoạt động, liệu chúng có đang bị quá tải hay không, và mức độ tích hợp tốt vào mạng. Những phép tính này sau đó được so sánh cho các peer hoạt động để tổ chức các router thành bốn tier — nhanh và công suất cao, công suất cao, không lỗi, và đang lỗi. Các ngưỡng cho những tier đó được xác định một cách động, và mặc dù chúng hiện tại sử dụng các thuật toán khá đơn giản, nhưng vẫn tồn tại các phương án thay thế.

Sử dụng dữ liệu hồ sơ này, chiến lược lựa chọn peer đơn giản nhất hợp lý là chọn ngẫu nhiên các peer từ tầng cao nhất (nhanh và dung lượng cao), và điều này hiện đang được triển khai cho client tunnel. Exploratory tunnel (được sử dụng cho quản lý netDb và tunnel) chọn ngẫu nhiên các peer từ tầng "không thất bại" (bao gồm cả các router ở các tầng 'tốt hơn'), cho phép peer lấy mẫu các router rộng rãi hơn, thực tế là tối ưu hóa việc lựa chọn peer thông qua [leo đồi](https://en.wikipedia.org/wiki/Hill_climbing) ngẫu nhiên. Tuy nhiên, chỉ riêng những chiến lược này vẫn rò rỉ thông tin về các peer trong tầng cao nhất của router thông qua các cuộc tấn công predecessor và thu thập netDb. Do đó, tồn tại nhiều giải pháp thay thế mà, mặc dù không cân bằng tải đều như vậy, nhưng sẽ giải quyết các cuộc tấn công do các lớp kẻ thù cụ thể thực hiện.

Bằng cách chọn một khóa ngẫu nhiên và sắp xếp các peer theo khoảng cách XOR của chúng từ khóa đó, thông tin bị rò rỉ sẽ giảm trong các cuộc tấn công predecessor và harvesting theo tỷ lệ lỗi của các peer và sự biến động của tầng. Một chiến lược đơn giản khác để đối phó với các cuộc tấn công harvesting netDb là chỉ cần cố định gateway tunnel đầu vào nhưng ngẫu nhiên hóa các peer xa hơn trong các tunnel. Để đối phó với các cuộc tấn công predecessor đối với những adversary mà client liên lạc, các endpoint tunnel đầu ra cũng sẽ giữ cố định. Việc lựa chọn peer nào để cố định tại điểm dễ bị tấn công nhất tất nhiên cần có giới hạn về thời gian, vì tất cả peer cuối cùng đều sẽ gặp lỗi, vì vậy nó có thể được điều chỉnh phản ứng hoặc tránh chủ động để mô phỏng thời gian trung bình đo được giữa các lần lỗi của các router khác. Hai chiến lược này có thể được kết hợp, sử dụng một peer cố định bị lộ và sắp xếp dựa trên XOR trong chính các tunnel. Một chiến lược cứng nhắc hơn sẽ cố định các peer chính xác và thứ tự của một tunnel tiềm năng, chỉ sử dụng các peer riêng lẻ nếu tất cả đều đồng ý tham gia theo cùng một cách mỗi lần. Điều này khác với sắp xếp dựa trên XOR ở chỗ predecessor và successor của mỗi peer luôn giống nhau, trong khi XOR chỉ đảm bảo thứ tự của chúng không thay đổi.

Như đã đề cập trước đó, I2P hiện tại (phiên bản 0.8) bao gồm chiến lược ngẫu nhiên phân tầng ở trên, với thứ tự dựa trên XOR. Thảo luận chi tiết hơn về cơ chế liên quan đến hoạt động tunnel, quản lý, và lựa chọn peer có thể được tìm thấy trong [tunnel spec](/docs/specs/tunnel-implementation/).

---

### Cơ sở dữ liệu mạng (netDb)

Như đã đề cập trước đó, netDb của I2P hoạt động để chia sẻ metadata của mạng. Điều này được mô tả chi tiết trong trang [cơ sở dữ liệu mạng](/docs/specs/common-structures/), nhưng một giải thích cơ bản có sẵn bên dưới.

Tất cả các router I2P đều chứa một netDb cục bộ, nhưng không phải tất cả router đều tham gia vào DHT hoặc phản hồi các truy vấn leaseset. Những router tham gia vào DHT và phản hồi các truy vấn leaseset được gọi là 'floodfill'. Các router có thể được cấu hình thủ công thành floodfill, hoặc tự động trở thành floodfill nếu chúng có đủ dung lượng và đáp ứng các tiêu chí khác để hoạt động ổn định.

Các I2P router khác sẽ lưu trữ dữ liệu của họ và tìm kiếm dữ liệu bằng cách gửi các truy vấn 'store' và 'lookup' đơn giản đến các floodfill. Nếu một floodfill router nhận được truy vấn 'store', nó sẽ truyền bá thông tin đến các floodfill router khác bằng cách sử dụng [thuật toán Kademlia](http://en.wikipedia.org/wiki/Kademlia). Các truy vấn 'lookup' hiện tại hoạt động khác nhau, để tránh một vấn đề bảo mật quan trọng. Khi thực hiện lookup, floodfill router sẽ không chuyển tiếp lookup đến các peer khác, mà sẽ luôn tự trả lời (nếu nó có dữ liệu được yêu cầu).

Có hai loại thông tin được lưu trữ trong cơ sở dữ liệu mạng.

- Một **RouterInfo** lưu trữ thông tin về một router I2P cụ thể và cách liên lạc với nó
- Một **LeaseSet** lưu trữ thông tin về một đích cụ thể (ví dụ: trang web I2P, máy chủ email...)

Tất cả thông tin này được ký bởi bên xuất bản và được xác minh bởi bất kỳ I2P router nào sử dụng hoặc lưu trữ thông tin đó. Ngoài ra, dữ liệu chứa thông tin thời gian, để tránh lưu trữ các mục cũ và các cuộc tấn công có thể xảy ra. Đây cũng là lý do tại sao I2P đi kèm với mã cần thiết để duy trì thời gian chính xác, thỉnh thoảng truy vấn một số máy chủ SNTP (mặc định là [pool.ntp.org](http://www.pool.ntp.org/) round robin) và phát hiện độ lệch thời gian giữa các router ở tầng vận chuyển.

Một số nhận xét bổ sung cũng quan trọng.

- **LeaseSet không được xuất bản và được mã hóa:**
  Người ta có thể chỉ muốn những người cụ thể có thể tiếp cận được một đích đến. Điều này có thể thực hiện bằng cách không xuất bản đích đến trong netDb. Tuy nhiên, bạn sẽ phải truyền đích đến bằng các phương tiện khác. Điều này được hỗ trợ bởi 'encrypted leaseSet'. Những leaseSet này chỉ có thể được giải mã bởi những người có quyền truy cập vào khóa giải mã.

- **Bootstrapping:**
  Bootstrapping netDb khá đơn giản. Một khi router có thể nhận được một routerInfo duy nhất của một peer có thể kết nối được, nó có thể truy vấn router đó để lấy tham chiếu đến các router khác trong mạng. Hiện tại, một số người dùng đăng các file routerInfo của họ lên website để cung cấp thông tin này. I2P tự động kết nối đến một trong những website này để thu thập các file routerInfo và bootstrap. I2P gọi quá trình bootstrap này là "reseeding".

- **Khả năng mở rộng tra cứu:**
  Các tra cứu trong mạng I2P là lặp lại, không phải đệ quy. Nếu tra cứu từ một floodfill thất bại, tra cứu sẽ được lặp lại với floodfill gần nhất tiếp theo. Floodfill không đệ quy hỏi floodfill khác để lấy dữ liệu. Các tra cứu lặp lại có thể mở rộng cho các mạng DHT lớn.

---

### Giao thức Truyền tải

Giao tiếp giữa các router cần cung cấp tính bảo mật và toàn vẹn chống lại các đối thủ bên ngoài trong khi xác thực rằng router được liên lạc chính là router cần nhận một thông điệp nhất định. Các chi tiết cụ thể về cách các router giao tiếp với nhau không quan trọng — ba giao thức riêng biệt đã được sử dụng tại các thời điểm khác nhau để cung cấp những yêu cầu cơ bản đó.

I2P hiện tại hỗ trợ hai giao thức truyền tải, [NTCP2](/docs/specs/ntcp2/) qua TCP, và [SSU2](/docs/specs/ssu2/) qua UDP. Các giao thức này đã thay thế các phiên bản trước đó, [NTCP](/docs/legacy/ssu/) và [SSU](/docs/legacy/ssu/), hiện đã không được khuyến nghị sử dụng. Cả hai giao thức đều hỗ trợ IPv4 và IPv6. Bằng cách hỗ trợ cả giao thức truyền tải TCP và UDP, I2P có thể vượt qua hầu hết các tường lửa một cách hiệu quả, bao gồm cả những tường lửa được thiết kế để chặn lưu lượng trong các chế độ kiểm duyệt hạn chế. NTCP2 và SSU2 được thiết kế để sử dụng các tiêu chuẩn mã hóa hiện đại, cải thiện khả năng chống nhận dạng lưu lượng, tăng hiệu quả và bảo mật, và làm cho việc vượt qua NAT mạnh mẽ hơn. Các router công bố từng giao thức truyền tải được hỗ trợ và địa chỉ IP trong cơ sở dữ liệu mạng. Các router có quyền truy cập vào mạng IPv4 và IPv6 công cộng thường sẽ công bố bốn địa chỉ, một địa chỉ cho mỗi sự kết hợp của NTCP2/SSU2 với IPv4/IPv6.

[SSU2](/docs/specs/ssu2/) hỗ trợ và mở rộng các mục tiêu của SSU. SSU2 có nhiều điểm tương đồng với các giao thức UDP hiện đại khác như Wireguard và QUIC. Ngoài việc truyền tải đáng tin cậy các thông điệp mạng qua UDP, SSU2 cung cấp các tiện ích chuyên biệt cho peer-to-peer, phát hiện địa chỉ IP hợp tác, phát hiện tường lửa và vượt qua NAT. Như được mô tả trong [thông số kỹ thuật SSU](/docs/legacy/ssu/):

> Mục tiêu của giao thức này là cung cấp khả năng truyền tải thông điệp an toàn, được xác thực, bán tin cậy và không theo thứ tự, chỉ để lộ một lượng dữ liệu tối thiểu dễ dàng nhận biết đối với các bên thứ ba. Nó nên hỗ trợ truyền thông độ tin cậy cao cũng như kiểm soát tắc nghẽn thân thiện với TCP và có thể bao gồm phát hiện PMTU. Nó nên có khả năng di chuyển dữ liệu lớn một cách hiệu quả với tốc độ đủ cho người dùng gia đình. Ngoài ra, nó nên hỗ trợ các kỹ thuật để giải quyết các trở ngại mạng, như hầu hết các NAT hoặc tường lửa.

[NTCP2](/docs/specs/ntcp2/) hỗ trợ và mở rộng các mục tiêu của NTCP. Nó cung cấp một cách truyền tải hiệu quả và được mã hóa hoàn toàn các thông điệp mạng qua TCP, và khả năng chống nhận dạng lưu lượng, sử dụng các tiêu chuẩn mã hóa hiện đại.

I2P hỗ trợ nhiều phương thức vận chuyển đồng thời. Một phương thức vận chuyển cụ thể cho kết nối đi ra được chọn bằng "bids" (đấu giá). Mỗi phương thức vận chuyển đưa ra giá thầu cho kết nối và giá trị tương đối của các giá thầu này quyết định mức độ ưu tiên. Các phương thức vận chuyển có thể trả lời với các giá thầu khác nhau, tùy thuộc vào việc đã có kết nối được thiết lập với peer hay chưa.

Các giá trị bid (ưu tiên) phụ thuộc vào cách triển khai và có thể thay đổi dựa trên điều kiện lưu lượng, số lượng kết nối và các yếu tố khác. Các router cũng công bố tùy chọn transport của chúng cho các kết nối đến trong cơ sở dữ liệu mạng dưới dạng "chi phí" transport cho mỗi transport và địa chỉ.

---

### Mật mã học

I2P sử dụng mã hóa tại nhiều tầng giao thức cho việc mã hóa, xác thực và xác minh. Các tầng giao thức chính bao gồm: transports, tunnel build messages, tunnel layer encryption, network database messages, và end-to-end (garlic) messages. Thiết kế ban đầu của I2P sử dụng một bộ nhỏ các nguyên thủy mã hóa mà vào thời điểm đó được coi là an toàn. Chúng bao gồm mã hóa bất đối xứng ElGamal, chữ ký DSA-SHA1, mã hóa đối xứng AES256/CBC, và hash SHA-256. Khi sức mạnh tính toán có sẵn tăng lên và nghiên cứu mã hóa phát triển đáng kể qua các năm, I2P cần nâng cấp các nguyên thủy và giao thức của mình. Do đó, chúng tôi đã thêm khái niệm "encryption types" và "signature types", và mở rộng các giao thức của chúng tôi để bao gồm các định danh này và chỉ ra sự hỗ trợ. Điều này cho phép chúng tôi định kỳ cập nhật và mở rộng hỗ trợ mạng cho mã hóa hiện đại và bảo vệ mạng cho tương lai với các nguyên thủy mới, mà không phá vỡ khả năng tương thích ngược hoặc yêu cầu "flag day" cho các cập nhật mạng. Một số signature và encryption types cũng được dành riêng cho mục đích thử nghiệm.

Các thuật toán mật mã hiện tại được sử dụng trong hầu hết các lớp giao thức là trao đổi khóa X25519, chữ ký EdDSA, mã hóa đối xứng được xác thực ChaCha20/Poly1305, và hash SHA-256. AES256 vẫn được sử dụng để mã hóa lớp tunnel. Những giao thức hiện đại này được sử dụng cho phần lớn giao tiếp mạng. Các thuật toán mật mã cũ hơn bao gồm ElGamal, ECDSA, và DSA-SHA1 vẫn tiếp tục được hỗ trợ bởi hầu hết các triển khai để tương thích ngược khi giao tiếp với các router cũ hơn. Một số giao thức cũ đã bị phản đối và/hoặc loại bỏ hoàn toàn. Trong tương lai gần, chúng tôi sẽ bắt đầu nghiên cứu việc di chuyển sang mã hóa và chữ ký post-quantum (PQ) hoặc hybrid-PQ để duy trì các tiêu chuẩn bảo mật mạnh mẽ của chúng tôi.

Những nguyên thủy mật mã này được kết hợp lại với nhau để cung cấp các lớp phòng thủ của I2P chống lại nhiều loại đối thủ khác nhau. Ở cấp độ thấp nhất, giao tiếp giữa các router được bảo vệ bởi bảo mật lớp giao vận. Các thông điệp [tunnel](#tunnels) được truyền qua các giao vận có mã hóa nhiều lớp riêng của chúng. Nhiều thông điệp khác được truyền bên trong các "garlic messages", cũng được mã hóa.

#### Tin nhắn Garlic

Garlic messages là một phần mở rộng của mã hóa phân lớp "onion", cho phép nội dung của một thông điệp đơn chứa nhiều "cloves" — các thông điệp được tạo thành hoàn chỉnh cùng với các hướng dẫn giao hàng riêng của chúng. Messages được bọc vào một garlic message bất cứ khi nào thông điệp có thể sẽ chuyển qua dưới dạng văn bản rõ qua một peer không được phép truy cập vào thông tin đó — ví dụ, khi một router muốn yêu cầu một router khác tham gia vào một tunnel, họ bọc yêu cầu đó bên trong một garlic, mã hóa garlic đó bằng khóa công khai của router nhận, và chuyển tiếp nó qua một tunnel. Một ví dụ khác là khi một client muốn gửi thông điệp đến một đích — router của người gửi sẽ bọc thông điệp dữ liệu đó (cùng với một số thông điệp khác) vào một garlic, mã hóa garlic đó bằng khóa công khai được công bố trong leaseSet của người nhận, và chuyển tiếp nó qua các tunnel thích hợp.

Các "hướng dẫn" được gắn với mỗi clove bên trong lớp mã hóa bao gồm khả năng yêu cầu clove được chuyển tiếp cục bộ, tới một router từ xa, hoặc tới một tunnel từ xa trên một router từ xa. Có các trường trong những hướng dẫn đó cho phép một peer yêu cầu việc giao hàng được trì hoãn cho đến một thời điểm nhất định hoặc điều kiện được đáp ứng, mặc dù chúng sẽ không được thực hiện cho đến khi [độ trễ không tầm thường](#variable-latency) được triển khai. Có thể định tuyến rõ ràng các garlic message qua bất kỳ số lượng hop nào mà không cần xây dựng tunnel, hoặc thậm chí định tuyến lại các tunnel message bằng cách bọc chúng trong garlic message và chuyển tiếp chúng qua một số hop trước khi giao chúng tới hop tiếp theo trong tunnel, nhưng những kỹ thuật đó hiện tại không được sử dụng trong implementation hiện có.

#### Thẻ Phiên

Là một hệ thống không đáng tin cậy, không có thứ tự và dựa trên thông điệp, I2P sử dụng kết hợp đơn giản của các thuật toán mã hóa bất đối xứng và đối xứng để cung cấp tính bảo mật và toàn vẹn dữ liệu cho các garlic message. Kết hợp ban đầu được gọi là ElGamal/AES+SessionTags, nhưng đó là cách mô tả quá dài dòng cho việc sử dụng đơn giản ElGamal 2048bit, AES256, SHA256 và nonce 32 byte. Mặc dù giao thức này vẫn được hỗ trợ, phần lớn mạng lưới đã chuyển sang giao thức mới, ECIES-X25519-AEAD-Ratchet. Giao thức này kết hợp X25519, ChaCha20/Poly1305, và PRNG đồng bộ để tạo ra nonce 32 byte. Cả hai giao thức sẽ được mô tả ngắn gọn bên dưới.

#### ElGamal/AES+SessionTags

Lần đầu tiên một router muốn mã hóa một thông điệp garlic tới một router khác, chúng mã hóa tài liệu khóa cho một khóa phiên AES256 bằng ElGamal và thêm payload được mã hóa AES256/CBC vào sau khối ElGamal được mã hóa đó. Ngoài payload được mã hóa, phần được mã hóa AES chứa độ dài payload, hash SHA256 của payload chưa được mã hóa, cũng như một số "session tags" — các nonce ngẫu nhiên 32 byte. Lần tiếp theo người gửi muốn mã hóa một thông điệp garlic tới một router khác, thay vì mã hóa ElGamal một khóa phiên mới, chúng đơn giản chọn một trong các session tags đã gửi trước đó và mã hóa AES payload như trước, sử dụng khóa phiên được dùng với session tag đó, được đặt trước bằng chính session tag đó. Khi một router nhận được một thông điệp được mã hóa garlic, chúng kiểm tra 32 byte đầu tiên để xem có khớp với một session tag có sẵn không — nếu có, chúng đơn giản giải mã AES thông điệp, nhưng nếu không, chúng giải mã ElGamal khối đầu tiên.

Mỗi session tag chỉ có thể được sử dụng một lần để ngăn chặn các đối thủ nội bộ không cần thiết liên kết các thông điệp khác nhau như đang được trao đổi giữa cùng các router. Người gửi của thông điệp được mã hóa ElGamal/AES+SessionTag sẽ chọn thời điểm và số lượng tag để giao, dự trữ trước cho người nhận đủ tag để bao phủ một loạt thông điệp. Các garlic message có thể phát hiện việc giao tag thành công bằng cách gói một thông điệp nhỏ bổ sung như một clove (một "delivery status message") — khi garlic message đến người nhận dự định và được giải mã thành công, thông điệp delivery status nhỏ này là một trong những clove được tiết lộ và có hướng dẫn cho người nhận gửi clove này trở lại cho người gửi ban đầu (thông qua inbound tunnel, tất nhiên). Khi người gửi ban đầu nhận được delivery status message này, họ biết rằng các session tag được gói trong garlic message đã được giao thành công.

Bản thân các session tag có thời gian tồn tại rất ngắn, sau đó chúng sẽ bị loại bỏ nếu không được sử dụng. Thêm vào đó, số lượng được lưu trữ cho mỗi khóa bị giới hạn, cũng như số lượng khóa - nếu quá nhiều khóa đến, các thông điệp mới hoặc cũ có thể bị loại bỏ. Bên gửi theo dõi xem các thông điệp sử dụng session tag có được gửi đến hay không, và nếu không có đủ giao tiếp thì nó có thể loại bỏ những thông điệp trước đó được cho là đã gửi đến đúng cách, quay trở lại sử dụng mã hóa ElGamal đầy đủ tốn kém.

#### ECIES-X25519-AEAD-Ratchet

ElGamal/AES+SessionTags yêu cầu chi phí bổ sung đáng kể theo nhiều cách. Việc sử dụng CPU cao vì ElGamal khá chậm. Băng thông quá mức vì số lượng lớn session tag phải được gửi trước, và vì khóa công khai ElGamal rất lớn. Việc sử dụng bộ nhớ cao do yêu cầu lưu trữ lượng lớn session tag. Độ tin cậy bị cản trở bởi việc mất mát trong quá trình gửi session tag.

ECIES-X25519-AEAD-Ratchet được thiết kế để giải quyết những vấn đề này. X25519 được sử dụng để trao đổi khóa. ChaCha20/Poly1305 được sử dụng cho mã hóa đối xứng có xác thực. Các khóa mã hóa được "double ratcheted" hoặc luân phiên định kỳ. Session tag được giảm từ 32 byte xuống 8 byte và được tạo bằng PRNG. Giao thức này có nhiều điểm tương đồng với signal protocol được sử dụng trong Signal và WhatsApp. Giao thức này cung cấp chi phí hoạt động thấp hơn đáng kể về CPU, RAM và băng thông.

Các session tag được tạo ra từ một PRNG đồng bộ xác định chạy ở cả hai đầu của phiên để tạo ra các session tag và session key. PRNG này là một HKDF sử dụng SHA-256 HMAC, và được khởi tạo từ kết quả X25519 DH. Các session tag không bao giờ được truyền trước; chúng chỉ được bao gồm cùng với thông điệp. Bên nhận lưu trữ một số lượng hạn chế các session key, được lập chỉ mục theo session tag. Bên gửi không cần lưu trữ bất kỳ session tag hoặc key nào vì chúng không được gửi trước; chúng có thể được tạo ra theo yêu cầu. Bằng cách giữ PRNG này đồng bộ gần như chính xác giữa bên gửi và bên nhận (bên nhận tính toán trước một cửa sổ của ví dụ 50 tag tiếp theo), việc định kỳ đóng gói một số lượng lớn tag sẽ được loại bỏ.

---

## Tương lai

Các giao thức của I2P hoạt động hiệu quả trên hầu hết các nền tảng, bao gồm cả điện thoại di động, và bảo mật cho hầu hết các mô hình mối đe dọa. Tuy nhiên, có một số lĩnh vực cần cải thiện thêm để đáp ứng nhu cầu của những người đối mặt với các đối thủ mạnh mẽ được nhà nước tài trợ, và để đối phó với các mối đe dọa từ sự tiến bộ liên tục của mật mã học và sức mạnh tính toán ngày càng tăng. Hai tính năng có thể có, restricted routes và variable latency, đã được jrandom đề xuất vào năm 2003. Mặc dù chúng tôi không còn kế hoạch triển khai các tính năng này, chúng được mô tả bên dưới.

### Hoạt động Route hạn chế

I2P là một overlay network được thiết kế để chạy trên một mạng chuyển mạch gói có chức năng, khai thác nguyên lý đầu cuối để cung cấp tính ẩn danh và bảo mật. Trong khi Internet không còn hoàn toàn tuân theo nguyên lý đầu cuối (do việc sử dụng NAT), I2P yêu cầu một phần đáng kể của mạng phải có thể tiếp cận được — có thể có một số peer dọc theo các cạnh chạy sử dụng các tuyến đường bị hạn chế, nhưng I2P không bao gồm thuật toán định tuyến phù hợp cho trường hợp suy biến khi hầu hết các peer không thể tiếp cận được. Tuy nhiên, nó sẽ hoạt động trên một mạng sử dụng thuật toán như vậy.

Hoạt động route bị hạn chế, nơi có các giới hạn về những peer nào có thể tiếp cận trực tiếp, có một số tác động chức năng và tính ẩn danh khác nhau, tùy thuộc vào cách các route bị hạn chế được xử lý. Ở mức cơ bản nhất, các route bị hạn chế tồn tại khi một peer đằng sau NAT hoặc tường lửa không cho phép các kết nối đến. Điều này đã được giải quyết phần lớn bằng cách tích hợp distributed hole punching vào lớp transport, cho phép những người đằng sau hầu hết NAT và tường lửa nhận được các kết nối không được yêu cầu mà không cần cấu hình gì. Tuy nhiên, điều này không giới hạn việc lộ địa chỉ IP của peer với các router bên trong mạng, vì chúng có thể đơn giản được giới thiệu đến peer thông qua introducer đã được xuất bản.

Ngoài việc xử lý chức năng các tuyến đường hạn chế, có hai cấp độ hoạt động hạn chế có thể được sử dụng để giới hạn việc tiết lộ địa chỉ IP của một người — sử dụng các tunnel dành riêng cho router để giao tiếp, và cung cấp 'client router'. Đối với cách thức đầu tiên, các router có thể xây dựng một nhóm tunnel mới hoặc tái sử dụng nhóm khám phá của chúng, công bố các gateway đầu vào đến một số tunnel đó như một phần của routerInfo thay vì các địa chỉ vận chuyển của chúng. Khi một peer muốn liên lạc với chúng, peer đó sẽ thấy các tunnel gateway trong netDb và chỉ cần gửi thông điệp có liên quan đến chúng thông qua một trong các tunnel đã được công bố. Nếu peer đằng sau tuyến đường hạn chế muốn trả lời, nó có thể làm vậy trực tiếp (nếu chúng sẵn sàng tiết lộ IP của mình cho peer) hoặc gián tiếp thông qua các tunnel đầu ra của chúng. Khi các router mà peer có kết nối trực tiếp muốn tiếp cận nó (để chuyển tiếp các thông điệp tunnel chẳng hạn), chúng chỉ đơn giản ưu tiên kết nối trực tiếp hơn tunnel gateway đã công bố. Khái niệm 'client router' đơn giản là mở rộng tuyến đường hạn chế bằng cách không công bố bất kỳ địa chỉ router nào. Router như vậy thậm chí không cần công bố routerInfo của chúng trong netDb, chỉ cần cung cấp routerInfo tự ký của chúng cho các peer mà nó liên hệ (cần thiết để chuyển các khóa công khai của router).

Có những đánh đổi đối với những người đứng sau các tuyến đường bị hạn chế, vì họ có thể sẽ ít tham gia vào các tunnel của người khác hơn, và các router mà họ kết nối tới có thể suy luận được các mẫu lưu lượng mà thông thường sẽ không bị lộ. Mặt khác, nếu chi phí của việc tiếp xúc đó ít hơn chi phí để có một IP khả dụng, thì có thể đáng giá. Điều này, tất nhiên, giả định rằng các peer mà router đứng sau tuyến đường bị hạn chế liên lạc không thù địch — hoặc mạng lưới đủ lớn để xác suất sử dụng peer thù địch để kết nối là đủ nhỏ, hoặc sử dụng các peer đáng tin cậy (và có thể tạm thời) thay thế.

Các tuyến đường hạn chế rất phức tạp, và mục tiêu tổng thể đã phần lớn bị từ bỏ. Một số cải tiến liên quan đã giảm đáng kể nhu cầu đối với chúng. Chúng tôi hiện hỗ trợ UPnP để tự động mở các cổng tường lửa. Chúng tôi hỗ trợ cả IPv4 và IPv6. SSU2 đã cải thiện việc phát hiện địa chỉ, xác định trạng thái tường lửa, và kỹ thuật đục lỗ NAT hợp tác. SSU2, NTCP2, và các kiểm tra tương thích địa chỉ đảm bảo rằng các hop tunnel có thể kết nối trước khi tunnel được xây dựng. GeoIP và nhận dạng quốc gia cho phép chúng tôi tránh các peer ở các quốc gia có tường lửa hạn chế. Hỗ trợ cho các router "ẩn" đằng sau những tường lửa đó đã được cải thiện. Một số triển khai cũng hỗ trợ kết nối đến các peer trên các mạng overlay như Yggdrasil.

### Độ Trễ Biến Đổi

Mặc dù phần lớn nỗ lực ban đầu của I2P tập trung vào giao tiếp độ trễ thấp, nó được thiết kế với các dịch vụ độ trễ thay đổi ngay từ đầu. Ở mức cơ bản nhất, các ứng dụng chạy trên I2P có thể cung cấp tính ẩn danh của giao tiếp độ trễ trung bình và cao trong khi vẫn pha trộn các mẫu lưu lượng của chúng với lưu lượng độ trễ thấp. Tuy nhiên, về mặt nội bộ, I2P có thể cung cấp giao tiếp độ trễ trung bình và cao của riêng mình thông qua garlic encryption — chỉ định rằng thông điệp nên được gửi sau một khoảng trễ nhất định, tại một thời điểm nhất định, sau khi một số lượng thông điệp nhất định đã được truyền, hoặc một chiến lược trộn khác. Với mã hóa nhiều lớp, chỉ có router mà clove tiết lộ yêu cầu trễ mới biết rằng thông điệp đó yêu cầu độ trễ cao, cho phép lưu lượng hòa trộn thêm với lưu lượng độ trễ thấp. Khi điều kiện tiên quyết truyền tải được đáp ứng, router giữ clove (bản thân nó có thể là một thông điệp garlic) chỉ cần chuyển tiếp nó như yêu cầu — đến một router, đến một tunnel, hoặc có thể nhất là đến một đích đến client từ xa.

Mục tiêu của các dịch vụ có độ trễ biến thiên đòi hỏi tài nguyên đáng kể cho các cơ chế store-and-forward để hỗ trợ nó. Các cơ chế này có thể và đang được hỗ trợ trong nhiều ứng dụng nhắn tin khác nhau, chẳng hạn như i2p-bote. Ở cấp độ mạng, các mạng thay thế như Freenet cung cấp những dịch vụ này. Chúng tôi đã quyết định không theo đuổi mục tiêu này ở cấp độ I2P router.

---

## Các Hệ Thống Tương Tự

Kiến trúc của I2P được xây dựng dựa trên các khái niệm về middleware định hướng thông điệp, cấu trúc liên kết của DHT, tính ẩn danh và mật mã học của free route mixnet, và khả năng thích ứng của mạng chuyển mạch gói. Giá trị không đến từ các khái niệm hay thuật toán mới lạ, mà từ việc kỹ thuật cẩn thận kết hợp các kết quả nghiên cứu của các hệ thống và bài báo hiện có. Mặc dù có một vài nỗ lực tương tự đáng được xem xét, cả về so sánh kỹ thuật và chức năng, hai trong số đó được đặc biệt nhấn mạnh ở đây — Tor và Freenet.

Xem thêm [Trang So sánh Mạng](/docs/overview/comparison/). Lưu ý rằng những mô tả này được viết bởi jrandom vào năm 2003 và có thể không còn chính xác hiện tại.

### Tor

*[website](https://www.torproject.org/)*

Thoạt nhìn, Tor và I2P có nhiều điểm tương đồng về chức năng và tính ẩn danh. Mặc dù việc phát triển I2P đã bắt đầu trước khi chúng tôi biết đến những nỗ lực giai đoạn đầu của Tor, nhiều bài học từ onion routing gốc và các nỗ lực của ZKS đã được tích hợp vào thiết kế của I2P. Thay vì xây dựng một hệ thống tập trung về cơ bản đáng tin cậy với các directory server, I2P có một network database tự tổ chức với mỗi peer đảm nhận trách nhiệm phân tích các router khác để xác định cách tận dụng tốt nhất các tài nguyên có sẵn. Một điểm khác biệt quan trọng khác là trong khi cả I2P và Tor đều sử dụng các đường dẫn phân lớp và có thứ tự (tunnel và circuit/stream), I2P về cơ bản là một mạng packet switched, trong khi Tor về cơ bản là mạng circuit switched, cho phép I2P định tuyến một cách minh bạch xung quanh tắc nghẽn hoặc các lỗi mạng khác, vận hành các đường dẫn dự phòng, và cân bằng tải dữ liệu trên các tài nguyên có sẵn. Trong khi Tor cung cấp chức năng outproxy hữu ích bằng cách cung cấp khám phá và lựa chọn outproxy tích hợp, I2P để các quyết định lớp ứng dụng như vậy cho các ứng dụng chạy trên I2P — thực tế, I2P thậm chí đã đưa chính thư viện streaming giống TCP ra lớp ứng dụng, cho phép các nhà phát triển thử nghiệm với các chiến lược khác nhau, tận dụng kiến thức cụ thể về miền của họ để cung cấp hiệu suất tốt hơn.

Từ góc độ ẩn danh, có nhiều điểm tương đồng khi so sánh các mạng lõi. Tuy nhiên, có một vài khác biệt chính. Khi đối phó với kẻ thù nội bộ hoặc hầu hết kẻ thù bên ngoài, các tunnel đơn hướng của I2P chỉ để lộ một nửa lượng dữ liệu lưu lượng so với các circuit hai chiều của Tor bằng cách chỉ đơn giản quan sát các luồng dữ liệu — một yêu cầu và phản hồi HTTP sẽ đi theo cùng một đường dẫn trong Tor, trong khi ở I2P các gói tin tạo nên yêu cầu sẽ đi ra thông qua một hoặc nhiều tunnel gửi đi và các gói tin tạo nên phản hồi sẽ quay trở lại thông qua một hoặc nhiều tunnel nhận về khác nhau. Mặc dù các chiến lược lựa chọn và sắp xếp peer của I2P sẽ giải quyết đầy đủ các cuộc tấn công tiền nhiệm (predecessor attacks), nếu cần phải chuyển sang các tunnel hai chiều, chúng ta có thể đơn giản xây dựng một tunnel nhận về và gửi đi dọc theo cùng các router.

Một vấn đề ẩn danh khác xuất hiện trong việc Tor sử dụng cơ chế tạo tunnel kiểu kính thiên văn, khi việc đếm gói tin đơn giản và đo lường thời gian khi các cell trong một mạch đi qua node của kẻ đối thủ sẽ để lộ thông tin thống kê về vị trí của kẻ đối thủ trong mạch đó. Cơ chế tạo tunnel một chiều của I2P với một thông điệp duy nhất giúp dữ liệu này không bị lộ. Việc bảo vệ vị trí trong tunnel là quan trọng, vì nếu không kẻ đối thủ có thể thực hiện một loạt các cuộc tấn công predecessor, intersection và xác nhận traffic mạnh mẽ.

Nhìn chung, Tor và I2P bổ sung cho nhau trong trọng tâm của chúng — Tor hướng tới việc cung cấp dịch vụ outproxy Internet ẩn danh tốc độ cao, trong khi I2P hướng tới việc cung cấp một mạng lưới phi tập trung có khả năng phục hồi. Về lý thuyết, cả hai đều có thể được sử dụng để đạt được cả hai mục đích, nhưng với nguồn lực phát triển hạn chế, chúng đều có điểm mạnh và điểm yếu riêng. Các nhà phát triển I2P đã xem xét những bước cần thiết để sửa đổi Tor nhằm tận dụng thiết kế của I2P, nhưng lo ngại về khả năng tồn tại của Tor trong điều kiện khan hiếm tài nguyên cho thấy rằng kiến trúc packet switching của I2P sẽ có thể khai thác các tài nguyên khan hiếm một cách hiệu quả hơn.

### Freenet

*[website](http://www.freenetproject.org/)*

Freenet đóng vai trò quan trọng trong giai đoạn đầu thiết kế I2P — chứng minh tính khả thi của một cộng đồng pseudonymous sôi động được chứa hoàn toàn trong mạng, cho thấy rằng có thể tránh được những nguy hiểm vốn có trong outproxy. Hạt giống đầu tiên của I2P bắt đầu như một lớp giao tiếp thay thế cho Freenet, cố gắng tách biệt sự phức tạp của giao tiếp điểm-tới-điểm có thể mở rộng, ẩn danh và bảo mật khỏi sự phức tạp của kho dữ liệu phân tán chống kiểm duyệt. Tuy nhiên theo thời gian, một số vấn đề về tính ẩn danh và khả năng mở rộng vốn có trong thuật toán của Freenet đã làm rõ rằng I2P nên tập trung nghiêm ngặt vào việc cung cấp lớp giao tiếp ẩn danh tổng quát, thay vì như một thành phần của Freenet. Qua nhiều năm, các nhà phát triển Freenet đã nhận ra những điểm yếu trong thiết kế cũ, thúc đẩy họ đề xuất rằng họ sẽ cần một lớp "premix" để cung cấp tính ẩn danh đáng kể. Nói cách khác, Freenet cần chạy trên một mixnet như I2P hoặc Tor, với các "client node" yêu cầu và xuất bản dữ liệu thông qua mixnet đến các "server node" sau đó tìm nạp và lưu trữ dữ liệu theo thuật toán lưu trữ dữ liệu phân tán heuristic của Freenet.

Chức năng của Freenet rất bổ sung cho I2P, vì Freenet tự nhiên cung cấp nhiều công cụ để vận hành các hệ thống độ trễ trung bình và cao, trong khi I2P tự nhiên cung cấp mạng trộn độ trễ thấp phù hợp để đảm bảo tính ẩn danh đầy đủ. Logic tách biệt mixnet khỏi kho dữ liệu phân tán chống kiểm duyệt vẫn có vẻ hiển nhiên từ góc độ kỹ thuật, tính ẩn danh, bảo mật và phân bổ tài nguyên, vì vậy hy vọng đội ngũ Freenet sẽ theo đuổi các nỗ lực theo hướng đó, nếu không đơn giản là tái sử dụng (hoặc giúp cải thiện, nếu cần thiết) các mixnet hiện có như I2P hoặc Tor.

---

## Phụ lục A: Tầng Ứng dụng

Bản thân I2P không thực sự làm nhiều việc — nó chỉ đơn giản gửi thông điệp đến các đích đến từ xa và nhận thông điệp nhắm đến các đích đến cục bộ — phần lớn công việc thú vị diễn ra ở các lớp phía trên nó. Xét riêng, I2P có thể được coi như một lớp IP ẩn danh và bảo mật, và [streaming library](#streaming-library) đi kèm như một triển khai của lớp TCP ẩn danh và bảo mật trên đó. Ngoài ra, [I2PTunnel](#i2ptunnel) cung cấp một hệ thống proxy TCP tổng quát để vào hoặc ra khỏi mạng I2P, cộng với nhiều ứng dụng mạng khác nhau cung cấp thêm chức năng cho người dùng cuối.

### Thư viện Streaming

Thư viện streaming I2P có thể được xem như một giao diện streaming chung (phản ánh TCP sockets), và việc triển khai hỗ trợ một [giao thức cửa sổ trượt](http://en.wikipedia.org/wiki/Sliding_Window_Protocol) với nhiều tối ưu hóa, để tính đến độ trễ cao trên I2P. Các stream riêng lẻ có thể điều chỉnh kích thước gói tin tối đa và các tùy chọn khác, mặc dù mặc định là 4KB nén có vẻ là một sự cân bằng hợp lý giữa chi phí băng thông của việc truyền lại các thông điệp bị mất và độ trễ của nhiều thông điệp.

Ngoài ra, xét đến chi phí tương đối cao của các thông điệp tiếp theo, giao thức của thư viện streaming để lập lịch và gửi thông điệp đã được tối ưu hóa để cho phép các thông điệp riêng lẻ được truyền chứa nhiều thông tin nhất có thể. Ví dụ, một giao dịch HTTP nhỏ được proxy thông qua thư viện streaming có thể hoàn thành trong một chuyến đi khứ hồi duy nhất — thông điệp đầu tiên gộp một SYN, FIN và payload nhỏ (một yêu cầu HTTP thường phù hợp) và phản hồi gộp SYN, FIN, ACK và payload nhỏ (nhiều phản hồi HTTP phù hợp). Mặc dù một ACK bổ sung phải được truyền để thông báo cho máy chủ HTTP rằng SYN/FIN/ACK đã được nhận, proxy HTTP cục bộ có thể gửi phản hồi đầy đủ đến trình duyệt ngay lập tức.

Tuy nhiên, nhìn chung, thư viện streaming có nhiều điểm tương đồng với sự trừu tượng hóa của TCP, với các cửa sổ trượt, thuật toán kiểm soát tắc nghẽn (cả slow start và congestion avoidance), và hành vi gói tin chung (ACK, SYN, FIN, RST, v.v.).

### Thư Viện Đặt Tên và Sổ Địa Chỉ

*Để biết thêm thông tin, xem trang [Đặt tên và Sổ địa chỉ](/docs/overview/naming/).*

*Được phát triển bởi: mihi, Ragnarok*

Việc đặt tên trong I2P đã là một chủ đề tranh luận thường xuyên ngay từ khi bắt đầu với những người ủng hộ trên khắp phổ các khả năng. Tuy nhiên, do nhu cầu vốn có của I2P về giao tiếp an toàn và hoạt động phi tập trung, hệ thống đặt tên kiểu DNS truyền thống rõ ràng bị loại bỏ, cũng như các hệ thống bỏ phiếu theo nguyên tắc "đa số quyết định". Thay vào đó, I2P được tích hợp sẵn một thư viện đặt tên chung và một triển khai cơ bản được thiết kế để hoạt động dựa trên ánh xạ tên cục bộ với destination, cũng như một ứng dụng bổ sung tùy chọn gọi là "Address Book" (Sổ địa chỉ). Address book là một hệ thống đặt tên an toàn, phân tán và có thể đọc được bằng con người, được điều khiển bởi web-of-trust, chỉ hy sinh yêu cầu tất cả tên có thể đọc được bằng con người phải là duy nhất toàn cầu bằng cách chỉ yêu cầu tính duy nhất cục bộ. Trong khi tất cả thông điệp trong I2P được định địa chỉ mật mã học bởi destination của chúng, những người khác nhau có thể có các mục address book cục bộ cho "Alice" mà tham chiếu đến các destination khác nhau. Mọi người vẫn có thể khám phá tên mới bằng cách nhập các address book đã xuất bản của các peer được chỉ định trong web of trust của họ, bằng cách thêm vào các mục được cung cấp thông qua bên thứ ba, hoặc (nếu một số người tổ chức một chuỗi address book đã xuất bản sử dụng hệ thống đăng ký ai đến trước được phục vụ trước) mọi người có thể chọn coi những address book này như name server, mô phỏng DNS truyền thống.

I2P không khuyến khích việc sử dụng các dịch vụ giống DNS, vì thiệt hại gây ra bởi việc chiếm đoạt một trang web có thể rất lớn — và các destination không an toàn không có giá trị gì. Bản thân DNSsec vẫn phụ thuộc vào các nhà đăng ký và certificate authority, trong khi với I2P, các yêu cầu gửi đến một destination không thể bị chặn bắt hoặc phản hồi bị giả mạo, vì chúng được mã hóa bằng public key của destination, và bản thân destination chỉ là một cặp public key và một certificate. Mặt khác, các hệ thống kiểu DNS cho phép bất kỳ name server nào trên đường dẫn tra cứu thực hiện các cuộc tấn công từ chối dịch vụ và giả mạo đơn giản. Việc thêm vào một certificate xác thực các phản hồi được ký bởi một certificate authority tập trung nào đó sẽ giải quyết nhiều vấn đề về nameserver thù địch nhưng vẫn để lại các cuộc tấn công replay cũng như các cuộc tấn công certificate authority thù địch.

Việc đặt tên theo kiểu bỏ phiếu cũng rất nguy hiểm, đặc biệt là do hiệu quả của các cuộc tấn công Sybil trong các hệ thống ẩn danh — kẻ tấn công có thể đơn giản tạo ra một số lượng peer tùy ý cao và "bỏ phiếu" với từng peer để chiếm quyền kiểm soát một tên nhất định. Các phương pháp proof-of-work có thể được sử dụng để làm cho danh tính không miễn phí, nhưng khi mạng lưới phát triển, tải cần thiết để liên lạc với mọi người để tiến hành bỏ phiếu trực tuyến là không khả thi, hoặc nếu không truy vấn toàn bộ mạng lưới, các tập hợp câu trả lời khác nhau có thể được tiếp cận.

Tuy nhiên, giống như Internet, I2P đang giữ thiết kế và vận hành của hệ thống đặt tên nằm ngoài tầng giao tiếp (giống như IP). Thư viện đặt tên đi kèm bao gồm một giao diện nhà cung cấp dịch vụ đơn giản mà các hệ thống đặt tên thay thế có thể kết nối vào, cho phép người dùng cuối quyết định loại đánh đổi về đặt tên mà họ muốn.

### I2PTunnel

*Phát triển bởi: mihi*

I2PTunnel có lẽ là ứng dụng client phổ biến và linh hoạt nhất của I2P, cho phép proxy chung chung cả vào và ra khỏi mạng I2P. I2PTunnel có thể được xem như bốn ứng dụng proxy riêng biệt — một "client" nhận các kết nối TCP đến và chuyển tiếp chúng đến một đích I2P nhất định, một "httpclient" (hay còn gọi là "eepproxy") hoạt động như một HTTP proxy và chuyển tiếp các yêu cầu đến đích I2P phù hợp (sau khi truy vấn dịch vụ đặt tên nếu cần thiết), một "server" nhận các kết nối I2P streaming đến trên một đích và chuyển tiếp chúng đến một TCP host+port nhất định, và một "httpserver" mở rộng "server" bằng cách phân tích các yêu cầu và phản hồi HTTP để cho phép hoạt động an toàn hơn. Có thêm một ứng dụng "socksclient", nhưng việc sử dụng nó không được khuyến khích vì những lý do đã đề cập trước đó.

I2P bản thân không phải là một mạng lưới outproxy — những lo ngại về tính ẩn danh và bảo mật vốn có trong một mix net chuyển tiếp dữ liệu vào và ra khỏi mix đã khiến thiết kế của I2P tập trung vào việc cung cấp một mạng lưới ẩn danh có khả năng đáp ứng nhu cầu của người dùng mà không cần tài nguyên bên ngoài. Tuy nhiên, ứng dụng I2PTunnel "httpclient" cung cấp một hook cho outproxying — nếu hostname được yêu cầu không kết thúc bằng ".i2p", nó sẽ chọn một điểm đến ngẫu nhiên từ một tập hợp outproxy do người dùng cung cấp và chuyển tiếp yêu cầu đến chúng. Những điểm đến này chỉ đơn giản là các instance I2PTunnel "server" được vận hành bởi các tình nguyện viên đã chủ động lựa chọn chạy outproxy — không ai là outproxy theo mặc định, và việc chạy một outproxy không tự động thông báo cho người khác proxy qua bạn. Mặc dù outproxy có những điểm yếu vốn có, chúng cung cấp một bằng chứng khái niệm đơn giản để sử dụng I2P và mang lại một số chức năng dưới một mô hình mối đe dọa có thể đủ cho một số người dùng.

I2PTunnel cho phép hầu hết các ứng dụng được sử dụng. Một "httpserver" chỉ đến máy chủ web cho phép bất kỳ ai chạy trang web ẩn danh của riêng họ (hoặc "I2P Site") — một máy chủ web được tích hợp sẵn với I2P cho mục đích này, nhưng có thể sử dụng bất kỳ máy chủ web nào. Bất kỳ ai cũng có thể chạy một "client" chỉ đến một trong những máy chủ IRC được lưu trữ ẩn danh, mỗi máy chủ đều chạy một "server" chỉ đến IRCd cục bộ của họ và giao tiếp giữa các IRCd qua các tunnel "client" riêng của chúng. Người dùng cuối cũng có các tunnel "client" chỉ đến các đích POP3 và SMTP của [I2Pmail](#i2pmail--susimail) (lần lượt chỉ đơn giản là các phiên bản "server" chỉ đến máy chủ POP3 và SMTP), cũng như các tunnel "client" chỉ đến máy chủ CVS của I2P, cho phép phát triển ẩn danh. Đôi khi mọi người thậm chí còn chạy proxy "client" để truy cập các phiên bản "server" chỉ đến máy chủ NNTP.

### I2PSnark

*I2PSnark được phát triển bởi: jrandom, và các cộng sự, chuyển đổi từ client [Snark](http://www.klomp.org/snark/) của [mjw](http://www.klomp.org/mark/)*

Được tích hợp sẵn trong bản cài đặt I2P, I2PSnark cung cấp một client BitTorrent ẩn danh đơn giản với khả năng đa torrent, hiển thị tất cả các chức năng thông qua giao diện web HTML thuần túy.

### I2Pmail / Susimail

*Được phát triển bởi: postman, susi23, mastiejaner*

I2Pmail là một dịch vụ hơn là một ứng dụng — postman cung cấp cả email nội bộ và bên ngoài với dịch vụ POP3 và SMTP thông qua các I2PTunnel instances truy cập một loạt các thành phần được phát triển với mastiejaner, cho phép mọi người sử dụng các mail client ưa thích của họ để gửi và nhận email một cách giả danh. Tuy nhiên, vì hầu hết các mail client đều tiết lộ thông tin nhận dạng đáng kể, I2P tích hợp sẵn web-based susimail client của susi23 đã được xây dựng đặc biệt với tính ẩn danh của I2P trong tâm trí. Dịch vụ I2Pmail/mail.i2p cung cấp lọc virus minh bạch cũng như ngăn chặn tấn công từ chối dịch vụ với hạn ngạch được tăng cường bằng hashcash. Ngoài ra, mỗi người dùng có quyền kiểm soát chiến lược batching của họ trước khi giao hàng thông qua các mail.i2p outproxies, được tách biệt khỏi các máy chủ SMTP và POP3 của mail.i2p — cả outproxies và inproxies đều giao tiếp với các máy chủ SMTP và POP3 của mail.i2p thông qua chính I2P, do đó việc xâm phạm những vị trí không ẩn danh đó không cho phép truy cập vào các tài khoản mail hoặc các mẫu hoạt động của người dùng.
