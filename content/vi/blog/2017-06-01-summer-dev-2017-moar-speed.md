---
title: "I2P Summer Dev 2017: Nhanh hơn nữa!"
date: 2017-06-01
author: "str4d"
description: "Summer Dev năm nay sẽ tập trung vào việc thu thập chỉ số và cải thiện hiệu năng cho mạng lưới."
categories: ["summer-dev"]
---

Lại đến thời điểm này trong năm! Chúng tôi đang khởi động chương trình phát triển mùa hè, trong đó chúng tôi tập trung vào một khía cạnh cụ thể của I2P để thúc đẩy nó tiến xa hơn. Trong ba tháng tới, chúng tôi sẽ khuyến khích cả những người đóng góp mới lẫn các thành viên cộng đồng hiện tại chọn một nhiệm vụ và thực hiện nó một cách vui vẻ!

Năm ngoái, chúng tôi tập trung vào việc giúp người dùng và nhà phát triển tận dụng I2P, bằng cách cải thiện bộ công cụ API và dành thêm sự quan tâm tới các ứng dụng chạy trên I2P. Năm nay, chúng tôi muốn cải thiện trải nghiệm người dùng bằng cách tập trung vào một khía cạnh ảnh hưởng đến tất cả mọi người: hiệu năng.

Mặc dù các mạng định tuyến củ hành (onion routing) thường được gọi là "mạng độ trễ thấp", việc định tuyến lưu lượng qua các máy tính bổ sung tạo ra chi phí phụ trội đáng kể. Thiết kế tunnel một chiều của I2P có nghĩa là theo mặc định, một vòng khứ hồi giữa hai Destinations (địa chỉ đích trong I2P) sẽ liên quan đến mười hai nút tham gia! Cải thiện hiệu năng của các nút tham gia này sẽ vừa giúp giảm độ trễ của các kết nối đầu-cuối, vừa nâng cao chất lượng của các tunnel trên toàn mạng.

## Nhanh hơn nữa!

Chương trình phát triển của chúng tôi trong năm nay sẽ gồm bốn thành phần:

### Measure

Chúng ta không thể biết mình có cải thiện hiệu năng hay không nếu không có mốc tham chiếu! Chúng tôi sẽ tạo một hệ thống đo lường để thu thập dữ liệu về mức độ sử dụng và hiệu năng của I2P theo cách thức bảo vệ quyền riêng tư, cũng như chuyển đổi nhiều công cụ đo hiệu năng để chạy qua I2P (ví dụ: iperf3).

### Đo lường

Có rất nhiều dư địa để cải thiện hiệu năng của mã nguồn hiện có của chúng tôi, ví dụ, nhằm giảm chi phí phụ trội khi tham gia vào tunnels. Chúng tôi sẽ xem xét các cải tiến tiềm năng đối với các nguyên thủy mật mã, các cơ chế truyền tải mạng (cả ở tầng liên kết và từ đầu đến cuối), lập hồ sơ peer, và lựa chọn lộ trình tunnel.

### Tối ưu hóa

Chúng tôi có một số đề xuất đang mở nhằm cải thiện khả năng mở rộng của mạng I2P (ví dụ: Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Chúng tôi sẽ làm việc trên các đề xuất này và bắt đầu triển khai những đề xuất đã được hoàn thiện trên các router mạng khác nhau.

### Tiếp tục

I2P là một mạng chuyển mạch gói, giống như internet mà nó chạy bên trên. Điều này mang lại cho chúng tôi sự linh hoạt đáng kể trong cách định tuyến các gói tin, cả vì hiệu năng lẫn quyền riêng tư. Phần lớn sự linh hoạt này vẫn chưa được khám phá! Chúng tôi muốn khuyến khích nghiên cứu về cách các kỹ thuật clearnet (mạng internet công khai ngoài các hệ thống ẩn danh) nhằm cải thiện băng thông có thể được áp dụng cho I2P, và cách chúng có thể ảnh hưởng đến quyền riêng tư của những người tham gia mạng.

## Take part in Summer Dev!

Chúng tôi còn rất nhiều ý tưởng khác muốn thực hiện trong các lĩnh vực này. Nếu bạn quan tâm đến việc phát triển phần mềm bảo vệ quyền riêng tư và ẩn danh, thiết kế các giao thức (mật mã hoặc loại khác), hoặc nghiên cứu những ý tưởng cho tương lai - hãy đến trò chuyện với chúng tôi trên IRC hoặc Twitter! Chúng tôi luôn sẵn sàng chào đón những người mới gia nhập cộng đồng của mình. Chúng tôi cũng sẽ gửi nhãn dán I2P tới tất cả các cộng tác viên mới tham gia!

Chúng tôi sẽ đăng ở đây trong suốt quá trình, nhưng bạn cũng có thể theo dõi tiến độ của chúng tôi và chia sẻ những ý tưởng, công việc của riêng bạn với hashtag #I2PSummer trên Twitter. Hãy cùng chào đón mùa hè!
