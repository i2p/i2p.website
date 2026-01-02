---
title: "Cải thiện sự chấp nhận I2P và Onboarding (quy trình khởi đầu cho người dùng mới) thông qua Jpackage, I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Các phương thức linh hoạt và mới nổi để cài đặt và nhúng I2P vào ứng dụng của bạn"
categories: ["general"]
---

Trong phần lớn thời gian tồn tại của I2P, nó là một ứng dụng chạy với sự hỗ trợ của Máy ảo Java đã được cài đặt sẵn trên nền tảng. Đây luôn là cách thông thường để phân phối các ứng dụng Java, nhưng điều đó dẫn đến quy trình cài đặt phức tạp đối với nhiều người. Phức tạp hơn nữa, “câu trả lời đúng” để giúp I2P dễ cài đặt trên một nền tảng bất kỳ có thể không giống như trên những nền tảng khác. Ví dụ, I2P khá đơn giản để cài đặt bằng các công cụ tiêu chuẩn trên các hệ điều hành dựa trên Debian và Ubuntu, vì chúng tôi có thể đơn giản liệt kê các thành phần Java cần thiết là “Required” trong gói của chúng tôi; tuy nhiên trên Windows hoặc OSX, không có hệ thống như vậy cho phép chúng tôi bảo đảm rằng một phiên bản Java tương thích đã được cài đặt.

Giải pháp hiển nhiên là tự quản lý việc cài đặt Java, nhưng điều đó từng là một vấn đề tự thân, nằm ngoài phạm vi của I2P. Tuy nhiên, trong các phiên bản Java gần đây, đã xuất hiện một tập tùy chọn mới có tiềm năng giải quyết vấn đề này cho nhiều phần mềm Java. Công cụ đầy hứa hẹn này có tên là **"Jpackage."**

## I2P-Zero và cài đặt I2P không có phụ thuộc

Nỗ lực đầu tiên rất thành công trong việc xây dựng một gói I2P không phụ thuộc (dependency-free) là I2P-Zero, được dự án Monero tạo ra ban đầu để sử dụng với tiền mã hóa Monero. Dự án này khiến chúng tôi rất hào hứng vì thành công của nó trong việc tạo ra một I2P router dùng cho mục đích chung, có thể dễ dàng được đóng gói kèm với một ứng dụng I2P. Đặc biệt trên Reddit, nhiều người bày tỏ họ ưa chuộng sự đơn giản khi thiết lập một I2P-Zero router.

Điều đó thực sự chứng minh cho chúng tôi rằng một Gói I2P không phụ thuộc, dễ cài đặt là hoàn toàn khả thi khi sử dụng các công cụ Java hiện đại, nhưng trường hợp sử dụng của I2P-Zero hơi khác với của chúng tôi. Nó phù hợp nhất cho các ứng dụng nhúng cần một I2P router có thể dễ dàng điều khiển thông qua cổng điều khiển tiện lợi ở cổng "8051". Bước tiếp theo của chúng tôi sẽ là điều chỉnh công nghệ này để áp dụng cho Ứng dụng I2P mục đích chung.

## Các thay đổi về bảo mật ứng dụng trên OSX ảnh hưởng đến trình cài đặt I2P IzPack

Vấn đề trở nên cấp bách hơn trong các phiên bản gần đây của Mac OSX, trong đó việc sử dụng bộ cài đặt "Classic" đi kèm ở định dạng .jar không còn đơn giản nữa. Điều này là vì ứng dụng không được "Notarized" bởi cơ quan có thẩm quyền của Apple và bị coi là rủi ro bảo mật. **Tuy nhiên**, Jpackage có thể tạo ra một tệp .dmg, tệp này có thể được cơ quan có thẩm quyền của Apple chứng thực, từ đó thuận tiện giải quyết vấn đề của chúng ta.

Trình cài đặt I2P .dmg mới, do Zlatinb tạo, giúp việc cài đặt I2P trên OSX dễ dàng hơn bao giờ hết, không còn yêu cầu người dùng tự cài Java và sử dụng các công cụ cài đặt tiêu chuẩn của OSX theo đúng cách thức khuyến nghị. Trình cài đặt .dmg mới giúp việc thiết lập I2P trên Mac OSX trở nên dễ dàng nhất từ trước tới nay.

Tải xuống [dmg](https://geti2p.net/en/download/mac)

## I2P của tương lai dễ cài đặt

Một trong những điều tôi nghe người dùng nói nhiều nhất là nếu I2P muốn được nhiều người sử dụng, nó cần phải dễ dùng đối với mọi người. Nhiều người trong số họ muốn một trải nghiệm người dùng kiểu "Tor Browser Like", để trích dẫn hoặc diễn giải lời của nhiều Redditor quen thuộc. Việc cài đặt không nên yêu cầu các bước "hậu cài đặt" phức tạp và dễ phát sinh lỗi. Nhiều người dùng mới không sẵn sàng xử lý cấu hình trình duyệt của họ một cách kỹ lưỡng và đầy đủ. Để giải quyết vấn đề này, chúng tôi đã tạo I2P Profile Bundle, cấu hình Firefox để nó tự động "hoạt động ngay" với I2P. Trong quá trình phát triển, nó đã bổ sung các tính năng bảo mật và cải thiện sự tích hợp với chính I2P. Trong phiên bản mới nhất, nó **cũng** đi kèm một I2P Router hoàn chỉnh, được Jpackage hỗ trợ. I2P Firefox Profile hiện là một bản phân phối I2P đầy đủ cho Windows, với phụ thuộc duy nhất còn lại là chính Firefox. Điều này sẽ mang lại mức độ thuận tiện chưa từng có cho người dùng I2P trên Windows.

Tải xuống [trình cài đặt](https://geti2p.net/en/download#windows)
