---
title: "How to offer your existing Web Site as an I2P eepSite"
date: 2019-06-02
author: "idk"
description: "Cung cấp một I2P Mirror (máy chủ phản chiếu)"
categories: ["tutorial"]
---

Bài viết blog này nhằm cung cấp hướng dẫn tổng quát về việc vận hành một bản phản chiếu của một dịch vụ clear-net (Internet công khai) dưới dạng một eepSite. Nó mở rộng nội dung của bài viết blog trước đó về các I2PTunnel tunnels cơ bản.

Thật không may, có lẽ không thể *hoàn toàn* bao quát mọi trường hợp có thể xảy ra khi cung cấp một trang web hiện có dưới dạng eepSite, đơn giản là vì có quá nhiều loại phần mềm phía máy chủ khác nhau, chưa kể đến những đặc thù trong thực tế của bất kỳ triển khai phần mềm cụ thể nào. Thay vào đó, tôi sẽ cố gắng truyền đạt, cụ thể nhất có thể, quy trình chung để chuẩn bị một dịch vụ cho việc triển khai lên eepWeb hoặc các dịch vụ ẩn khác.

Phần lớn của hướng dẫn này sẽ coi người đọc như một người tham gia đối thoại; cụ thể, khi tôi thực sự muốn nhấn mạnh, tôi sẽ trực tiếp xưng hô với người đọc (tức là dùng "you" thay vì "one") và tôi sẽ thường xuyên mở đầu các phần bằng những câu hỏi mà tôi nghĩ người đọc có thể đang tự hỏi. Xét cho cùng, đây là một "quy trình" mà một quản trị viên phải tự coi mình đang "tham gia" vào, giống như khi vận hành bất kỳ dịch vụ nào khác.

**MIỄN TRỪ TRÁCH NHIỆM:**

Mặc dù điều đó sẽ rất tuyệt, nhưng có lẽ không thể để tôi đưa ra hướng dẫn cụ thể cho mọi loại phần mềm mà người ta có thể dùng để lưu trữ trang web. Vì vậy, hướng dẫn này đòi hỏi một số giả định từ phía người viết và yêu cầu người đọc có tư duy phản biện cùng lẽ thường. Nói rõ hơn, **tôi giả định rằng người theo dõi hướng dẫn này đã vận hành một dịch vụ trên clear-web (web công khai) có thể liên kết với một danh tính hoặc tổ chức thực** và do đó chỉ đơn thuần cung cấp quyền truy cập ẩn danh chứ không ẩn danh hóa chính họ.

Vì vậy, **nó tuyệt đối không hề cố gắng ẩn danh hóa** một kết nối từ máy chủ này đến máy chủ khác. Nếu bạn muốn vận hành một hidden service (dịch vụ ẩn) mới, không thể truy vết, lưu trữ nội dung không gắn với bạn, thì bạn không nên thực hiện điều đó từ chính máy chủ clearnet (Internet công khai) của mình hoặc ngay tại nhà mình.
