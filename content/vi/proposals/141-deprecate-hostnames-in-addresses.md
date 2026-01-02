---
title: "Khuyến cáo không sử dụng tên miền trong địa chỉ router"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Closed"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Tổng quan

Kể từ phiên bản 0.9.32, cập nhật đặc tả netdb để khuyến cáo không sử dụng tên miền trong thông tin router, hoặc chính xác hơn là trong các địa chỉ router cá nhân. Trong tất cả các triển khai I2P, các router công bố được cấu hình với tên miền nên thay thế tên miền bằng IP trước khi công bố, và các router khác nên bỏ qua các địa chỉ có tên miền. Các router không nên thực hiện tra cứu DNS cho các tên miền đã công bố.

## Động lực

Tên miền đã được cho phép trong địa chỉ router ngay từ đầu I2P. Tuy nhiên, rất ít router công bố tên miền, vì nó yêu cầu cả tên miền công cộng (mà ít người dùng có), và cấu hình thủ công (mà ít người dùng bỏ công để làm). Trong một mẫu gần đây, 0.7% router đã công bố tên miền.

Mục đích ban đầu của tên miền là giúp người dùng với IP thay đổi thường xuyên và dịch vụ DNS động (như http://dyn.com/dns/) không bị mất kết nối khi IP của họ thay đổi. Tuy nhiên, khi đó mạng lưới nhỏ và thời gian hết hạn thông tin router lâu hơn. Thêm vào đó, mã Java không có logic hoạt động để khởi động lại router hoặc công bố lại thông tin router khi IP địa phương thay đổi.

Cũng vậy, từ đầu, I2P không hỗ trợ IPv6, vì vậy sự phức tạp của việc phân giải một tên miền đến địa chỉ IPv4 hoặc IPv6 không tồn tại.

Trong Java I2P, luôn là một thách thức để chuyển một tên miền cấu hình ra cả hai phương tiện công bố, và tình huống càng trở nên phức tạp hơn với IPv6. Không rõ liệu một máy chủ kép nên công bố cả tên miền và một địa chỉ IPv6 thực hay không. Tên miền được công bố cho địa chỉ SSU nhưng không phải địa chỉ NTCP.

Gần đây, các vấn đề DNS đã được đề cập (cả gián tiếp và trực tiếp) qua nghiên cứu tại Georgia Tech. Các nhà nghiên cứu đã chạy một số lượng lớn các floodfills với tên miền đã công bố. Vấn đề ngay lập tức là đối với một số nhỏ người dùng có thể có DNS địa phương bị hỏng, nó khiến I2P bị treo hoàn toàn.

Vấn đề lớn hơn là DNS nói chung, và cách DNS (dù chủ động hay bị động) có thể được sử dụng để đếm nhanh chóng mạng lưới, đặc biệt nếu các router công bố là floodfill. Các tên miền không hợp lệ hoặc các phản hồi DNS không đáp ứng, chậm, hoặc ác ý có thể được sử dụng cho các cuộc tấn công thêm. EDNS0 có thể cung cấp thêm các kịch bản tấn công hoặc đếm. DNS cũng có thể cung cấp các cách tấn công dựa trên thời gian tra cứu, tiết lộ thời gian kết nối router-to-router, giúp xây dựng đồ thị kết nối, ước tính lưu lượng, và các suy luận khác.

Ngoài ra, nhóm Georgia Tech, dẫn đầu bởi David Dagon, đã đưa ra một số lo ngại với DNS trong các ứng dụng tập trung vào quyền riêng tư. Tra cứu DNS thường được thực hiện bởi thư viện cấp thấp, không được kiểm soát bởi ứng dụng. Các thư viện này không được thiết kế cụ thể cho ẩn danh; có thể không cung cấp kiểm soát chi tiết bởi ứng dụng; và đầu ra của chúng có thể bị dấu vân tay. Các thư viện Java đặc biệt có thể có vấn đề, nhưng đây không chỉ là vấn đề của Java. Một số thư viện sử dụng truy vấn DNS ANY mà có thể bị từ chối. Tất cả điều này được làm lo ngại hơn bởi sự hiện diện rộng rãi của giám sát DNS thụ động và truy vấn có sẵn cho nhiều tổ chức. Tất cả giám sát và tấn công DNS là ngoài băng từ quan điểm của các router I2P và chỉ yêu cầu ít hoặc không có tài nguyên trong mạng I2P, và không cần chỉnh sửa các triển khai hiện có.

Trong khi chúng tôi chưa hoàn toàn suy nghĩ kỹ về các vấn đề có thể, bề mặt tấn công dường như rất lớn. Có những cách khác để đếm mạng lưới và thu thập dữ liệu liên quan, nhưng các cuộc tấn công DNS có thể dễ hơn nhiều, nhanh hơn và khó phát hiện hơn.

Các triển khai router có thể, về lý thuyết, chuyển sang sử dụng một thư viện DNS của bên thứ ba tinh vi, nhưng điều đó sẽ khá phức tạp, là một gánh nặng bảo trì và nằm ngoài phạm vi chuyên môn chủ chốt của các nhà phát triển I2P.

Các giải pháp tức thời được triển khai cho Java 0.9.31 bao gồm sửa lỗi treo, tăng thời gian bộ nhớ đệm DNS, và triển khai một bộ nhớ đệm tiêu cực DNS. Tất nhiên, việc tăng thời gian bộ nhớ đệm làm giảm lợi ích của việc có tên miền trong thông tin router ngay từ đầu.

Tuy nhiên, những thay đổi này chỉ là Biện pháp giảm nhẹ ngắn hạn và không giải quyết các vấn đề cơ bản trên. Do đó, cách sửa đơn giản nhất và hoàn chỉnh nhất là cấm tên miền trong thông tin router, do đó loại bỏ các truy vấn DNS cho chúng.


## Thiết kế

Đối với mã công bố thông tin router, người triển khai có hai lựa chọn, hoặc là vô hiệu/bỏ tùy chọn cấu hình cho tên miền, hoặc là chuyển đổi các tên miền đã cấu hình sang IP tại thời gian công bố. Trong cả hai trường hợp, các router nên công bố lại ngay lập tức khi IP của họ thay đổi.

Đối với mã xác thực thông tin router và kết nối truyền thông, người triển khai nên bỏ qua địa chỉ router chứa tên miền, và sử dụng các địa chỉ đã công bố khác chứa IP, nếu có. Nếu không có địa chỉ nào trong thông tin router chứa IPs, router không nên kết nối với router đã công bố. Không trường hợp nào router nên thực hiện truy vấn DNS cho tên miền đã công bố, dù trực tiếp hay qua một thư viện cơ bản.

## Thông số kỹ thuật

Thay đổi thông số kỹ thuật truyền thông NTCP và SSU để chỉ ra rằng tham số "host" phải là một IP, không phải tên miền, và rằng các router nên bỏ qua các địa chỉ router riêng lẻ chứa tên miền.

Điều này cũng áp dụng cho các tham số "ihost0", "ihost1", và "ihost2" trong địa chỉ SSU. Các router nên bỏ qua các địa chỉ người giới thiệu chứa tên miền.


## Ghi chú

Đề xuất này không đề cập đến tên miền cho các máy chủ reseed. Mặc dù các truy vấn DNS cho các máy chủ reseed ít thường xuyên hơn nhiều, chúng vẫn có thể là một vấn đề. Nếu cần, điều này có thể được sửa đơn giản bằng cách thay thế tên miền bằng các IP trong danh sách các URL đã mã hóa cứng; không yêu cầu thay đổi đặc tả hoặc mã.

## Chuyển đổi

Đề xuất này có thể được thực hiện ngay lập tức, mà không cần một quá trình chuyển đổi dần dần, bởi vì rất ít router công bố tên miền, và những router đó thường không công bố tên miền trong tất cả các địa chỉ.

Các router không cần kiểm tra phiên bản đã công bố của router trước khi quyết định bỏ qua tên miền, và không cần một phát hành phối hợp hoặc chiến lược chung trên toàn bộ các triển khai router khác nhau.

Đối với những router vẫn công bố tên miền, chúng sẽ nhận được ít kết nối đầu vào hơn, và có thể cuối cùng gặp khó khăn trong việc xây dựng đường hầm đầu vào.

Để giảm thiểu tác động thêm, những người triển khai có thể bắt đầu bằng cách bỏ qua địa chỉ router với tên miền chỉ đối với các router floodfill, hoặc đối với các router với phiên bản đã công bố ít hơn 0.9.32, và bỏ qua tên miền cho tất cả các router trong một phát hành sau.
