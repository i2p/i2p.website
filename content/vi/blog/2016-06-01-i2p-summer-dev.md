---
title: "I2P Phát triển Mùa hè"
date: 2016-06-01
author: "str4d"
description: "Chúng tôi vui mừng thông báo rằng mùa hè này, I2P sẽ bắt đầu một chương trình phát triển nhằm cải thiện hệ sinh thái phần mềm bảo vệ quyền riêng tư cho cả các nhà phát triển và người dùng."
categories: ["summer-dev"]
---

Trong vài năm qua, nhu cầu người dùng tự kiểm soát dữ liệu của mình ngày càng trở nên rõ ràng. Đã có những tiến bộ vượt bậc trong vấn đề này nhờ sự phát triển của các ứng dụng nhắn tin như Signal và các hệ thống lưu trữ tệp như Tahoe-LAFS. Nỗ lực đang diễn ra của Let's Encrypt nhằm mang HTTPS đến toàn thế giới cũng đang dần được phổ biến.

Nhưng việc tích hợp quyền riêng tư và tính ẩn danh vào các ứng dụng không hề đơn giản. Phần lớn phần mềm mà mọi người sử dụng hằng ngày không được thiết kế để bảo vệ quyền riêng tư, và các công cụ sẵn có cho nhà phát triển nói chung không dễ sử dụng. Bản khảo sát OnionScan mới được công bố đem lại cái nhìn về việc ngay cả những người dùng am hiểu kỹ thuật cũng có thể dễ dàng cấu hình sai dịch vụ của họ đến mức nào, khiến mục tiêu của họ bị phản tác dụng hoàn toàn.

## Giúp các nhà phát triển giúp người dùng của họ

Chúng tôi vui mừng thông báo rằng mùa hè năm nay, I2P sẽ khởi động một chương trình phát triển nhằm cải thiện hệ sinh thái phần mềm bảo vệ quyền riêng tư. Mục tiêu của chúng tôi là giúp mọi việc trở nên dễ dàng hơn cho cả các nhà phát triển muốn tận dụng I2P trong ứng dụng của họ, cũng như cho người dùng đang cố gắng cấu hình và chạy ứng dụng của họ thông qua I2P.

Mùa hè này, chúng tôi sẽ tập trung thời gian vào ba lĩnh vực bổ trợ cho nhau:

### June: APIs

Vào tháng Sáu, chúng tôi sẽ cập nhật các thư viện khác nhau hiện có để giao tiếp với I2P. Năm nay, chúng tôi đã đạt được những tiến bộ đáng kể trong việc mở rộng SAM API với các tính năng bổ sung, chẳng hạn như hỗ trợ datagram (gói dữ liệu phi kết nối) và cổng. Chúng tôi dự định giúp các tính năng này dễ sử dụng trong các thư viện C++ và Python của chúng tôi.

Chúng tôi cũng sẽ sớm giúp các nhà phát triển Java và Android dễ dàng hơn nhiều trong việc thêm hỗ trợ I2P vào các ứng dụng của họ. Hãy theo dõi!

### Tháng Sáu: các API

Trong tháng Bảy, chúng tôi sẽ làm việc với các ứng dụng đã bày tỏ quan tâm đến việc bổ sung hỗ trợ cho I2P. Hiện có một số ý tưởng rất hay đang được phát triển trong lĩnh vực quyền riêng tư, và chúng tôi muốn giúp các cộng đồng của họ tận dụng hơn một thập kỷ nghiên cứu và phát triển về tính ẩn danh ngang hàng (peer-to-peer). Việc mở rộng các ứng dụng này để hoạt động gốc qua I2P là một bước tiến tốt cho khả năng sử dụng, và trong quá trình đó sẽ cải thiện cách các ứng dụng này quan niệm và xử lý thông tin người dùng.

### Tháng 7: Ứng dụng

Cuối cùng, vào tháng Tám, chúng tôi sẽ chuyển sự chú ý sang các ứng dụng đi kèm trong I2P và danh mục plugin rộng hơn. Một số trong đó rất cần được chăm chút thêm để thân thiện với người dùng hơn, cũng như sửa các lỗi còn tồn đọng! Chúng tôi hy vọng những người ủng hộ I2P lâu năm sẽ hài lòng với kết quả của công việc này.

## Take part in Summer Dev!

Chúng tôi còn rất nhiều ý tưởng cho những việc muốn thực hiện trong các lĩnh vực này. Nếu bạn quan tâm đến việc tham gia phát triển phần mềm bảo vệ quyền riêng tư và ẩn danh, thiết kế các trang web hoặc giao diện dễ sử dụng, hoặc viết hướng dẫn cho người dùng, hãy đến trò chuyện với chúng tôi trên IRC hoặc Twitter! Chúng tôi luôn vui mừng chào đón những người mới vào cộng đồng của mình. Chúng tôi sẽ gửi sticker I2P đến tất cả các cộng tác viên mới tham gia!

Tương tự, nếu bạn là một nhà phát triển ứng dụng muốn được hỗ trợ tích hợp I2P, hoặc thậm chí chỉ muốn trò chuyện về các khái niệm hay chi tiết: hãy liên hệ! Nếu bạn muốn tham gia vào tháng Ứng dụng vào tháng Bảy của chúng tôi, hãy liên hệ với @GetI2P, @i2p hoặc @str4d trên Twitter. Bạn cũng có thể tìm chúng tôi tại kênh #i2p-dev trên OFTC hoặc FreeNode.

Chúng tôi sẽ cập nhật tại đây trong quá trình thực hiện, nhưng bạn cũng có thể theo dõi tiến trình của chúng tôi và chia sẻ ý tưởng cũng như công việc của riêng bạn với hashtag #I2PSummer trên Twitter. Cùng chào đón mùa hè!
