---
title: "Đề xuất I2P #166: Loại Đường hầm Nhận diện/Chủ nhà Nổi bật"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Open"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
---

### Đề xuất Loại Đường hầm Proxy HTTP Nhận diện Chủ nhà

Đây là một đề xuất để giải quyết “Vấn đề Nhận diện Chia sẻ” khi sử dụng HTTP qua I2P thông thường bằng cách giới thiệu một loại đường hầm proxy HTTP mới. Loại đường hầm này có hành vi bổ sung nhằm ngăn chặn hoặc hạn chế tính hữu ích của việc theo dõi được thực hiện bởi các nhà vận hành dịch vụ ẩn có thể thân thiện, chống lại tác nhân người dùng (trình duyệt) và chính Ứng dụng Khách hàng I2P.

#### “Vấn đề Nhận diện Chia sẻ” là gì?

“Vấn đề Nhận diện Chia sẻ” xảy ra khi một tác nhân người dùng trên mạng phủ có địa chỉ mã hóa chia sẻ một nhận diện mã hóa với một tác nhân người dùng khác. Điều này xảy ra, ví dụ, khi Firefox và GNU Wget đều được cấu hình để sử dụng cùng một Proxy HTTP.

Trong kịch bản này, máy chủ có thể thu thập và lưu trữ địa chỉ mã hóa (Destination) được sử dụng để trả lời cho hoạt động. Nó có thể xem đây là một “Dấu Vân tay” luôn luôn 100% độc nhất, vì nó có nguồn gốc mã hóa. Điều này có nghĩa là độ liên kết quan sát được bởi Vấn đề Nhận diện Chia sẻ là hoàn hảo.

Nhưng liệu nó có phải là một vấn đề?
^^^^^^^^^^^^^^^^^^^^

Vấn đề nhận diện chia sẻ là một vấn đề khi các tác nhân người dùng nói cùng giao thức mong muốn sự không liên kết. `Nó được đề cập lần đầu trong
ngữ cảnh của HTTP trong luồng Reddit này <https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/>`__, với các bình luận bị xóa có thể truy cập nhờ
`pullpush.io <https://api.pullpush.io/reddit/search/comment/?link_id=579idi>`__. *Lúc đó* tôi là một trong những người phản hồi tích cực nhất, và *lúc đó* tôi tin rằng vấn đề này nhỏ. Trong 8 năm qua, tình hình và quan điểm của tôi đã thay đổi, tôi hiện tin rằng mối đe dọa do sự tương quan đích đáng áp đặt đáng kể khi nhiều trang web ở vị trí “profiling” người dùng cụ thể hơn.

Cuộc tấn công này có ngưỡng đầu vào rất thấp. Nó chỉ yêu cầu rằng một nhà vận hành dịch vụ ẩn vận hành nhiều dịch vụ. Đối với các cuộc tấn công vào các lượt truy cập đương thời (thăm nhiều trang cùng một lúc), đây là yêu cầu duy nhất. Đối với liên kết không đương thời, một trong những dịch vụ đó phải là một dịch vụ có “tài khoản” thuộc về một người dùng duy nhất bị theo dõi.

Hiện tại, bất kỳ nhà vận hành dịch vụ nào lưu trữ tài khoản người dùng sẽ có thể tương quan chúng với hoạt động trên bất kỳ trang nào họ kiểm soát bằng cách khai thác Vấn đề Nhận diện Chia sẻ. Mastodon, Gitlab, hoặc thậm chí các diễn đàn đơn giản có thể là kẻ tấn công được ngụy trang miễn là họ vận hành hơn một dịch vụ và có quan tâm đến việc tạo hồ sơ cho người dùng. Việc giám sát này có thể được thực hiện nhằm mục đích rình rập, kiếm lợi tài chính hoặc lý do liên quan đến tình báo. Hiện tại có hàng tá các nhà vận hành lớn có thể thực hiện cuộc tấn công này và thu thập dữ liệu có ý nghĩa từ nó. Chúng ta chủ yếu tin tưởng rằng họ sẽ không làm vậy, nhưng những người chơi không quan tâm đến ý kiến của chúng ta có thể dễ dàng xuất hiện.

Điều này liên quan trực tiếp đến một hình thức khá cơ bản của việc xây dựng hồ sơ trên web rõ ràng nơi các tổ chức có thể tương quan tương tác trên trang của họ với các tương tác trên các mạng họ kiểm soát. Trên I2P, vì địa chỉ đích mã hóa là duy nhất, kỹ thuật này đôi khi có thể còn đáng tin cậy hơn, mặc dù không có sức mạnh bổ sung của định vị địa lý.

Nhận diện Chia sẻ không hữu ích đối với một người dùng đang sử dụng I2P chỉ để làm mờ định vị địa lý. Nó cũng không thể được sử dụng để phá vỡ định tuyến của I2P. Đây chỉ là một vấn đề về quản lý nhận diện ngữ cảnh.

- Không thể sử dụng vấn đề nhận diện chia sẻ để định vị địa lý người dùng I2P.
- Không thể sử dụng vấn đề nhận diện chia sẻ để liên kết các phiên I2P nếu chúng không đương thời.

Tuy nhiên, có thể sử dụng nó để làm suy giảm tính ẩn danh của người dùng I2P trong những hoàn cảnh có thể rất phổ biến. Một lý do chúng phổ biến là chúng ta khuyến khích sử dụng Firefox, một trình duyệt web hỗ trợ hoạt động “Tabbed”.

- Luôn luôn có thể tạo ra một dấu vân tay từ vấn đề nhận diện chia sẻ trong bất kỳ trình duyệt web nào hỗ trợ yêu cầu tài nguyên của bên thứ ba.
- Việc vô hiệu hóa Javascript không đạt được **gì** đối với vấn đề nhận diện chia sẻ.
- Nếu có thể thiết lập một liên kết giữa các phiên không đương thời chẳng hạn như bằng cách nhận diện trình duyệt truyền thống, thì nhận diện chia sẻ có thể được áp dụng theo chiều chuyển đổi, tiềm năng cho phép một chiến lược liên kết không đương thời.
- Nếu có thể thiết lập một liên kết giữa hoạt động mạng thông thường và một nhận diện I2P, ví dụ, nếu mục tiêu đang đăng nhập vào một trang web với cả một sự hiện diện I2P và mạng thông thường trên cả hai bên, nhận diện chia sẻ có thể được áp dụng theo chiều chuyển đổi, tiềm năng dẫn đến mất hoàn toàn tính ẩn danh.

Cách bạn đánh giá mức độ nghiêm trọng của vấn đề nhận diện chia sẻ khi áp dụng cho proxy HTTP I2P phụ thuộc vào việc bạn (hoặc hơn thế, một “người dùng” với các kỳ vọng có thể chưa được thông tin đầy đủ) nghĩ “nhận diện ngữ cảnh” cho ứng dụng nằm ở đâu. Có một số khả năng:

1. HTTP là cả Ứng dụng và Nhận diện Ngữ cảnh - Đây là cách nó hoạt động hiện tại. Tất cả ứng dụng HTTP chia sẻ một nhận diện.
2. Quá trình là Ứng dụng và Nhận diện Ngữ cảnh - Đây là cách nó hoạt động khi một ứng x
