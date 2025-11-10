---
title: "New I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Nhiều bản triển khai I2P router mới đang xuất hiện, bao gồm emissary viết bằng Rust và go-i2p viết bằng Go, mang lại những khả năng mới cho việc nhúng và đa dạng hóa mạng lưới."
---

Đây là thời điểm đầy hứng khởi đối với việc phát triển I2P; cộng đồng của chúng ta đang lớn mạnh và hiện đã có nhiều nguyên mẫu I2P router mới, hoạt động đầy đủ, xuất hiện! Chúng tôi rất phấn khởi về bước phát triển này và mong được chia sẻ tin vui với bạn.

## Việc này giúp ích cho mạng lưới như thế nào?

Việc phát triển các router I2P giúp chúng tôi chứng minh rằng các tài liệu đặc tả có thể được dùng để tạo ra các router I2P mới, mở ra khả năng áp dụng các công cụ phân tích mới đối với mã nguồn, và nhìn chung cải thiện bảo mật cũng như khả năng tương tác của mạng. Sự tồn tại của nhiều router I2P đồng nghĩa với việc các lỗi tiềm ẩn không đồng nhất; một cuộc tấn công vào một router có thể không hiệu quả trên một router khác, qua đó tránh được vấn đề monoculture (hệ sinh thái đồng nhất). Tuy nhiên, có lẽ triển vọng thú vị nhất về dài hạn lại là khả năng nhúng.

## Nhúng là gì?

Trong bối cảnh I2P, nhúng là cách đưa trực tiếp một router I2P vào một ứng dụng khác, mà không cần một router độc lập chạy nền. Đây là một cách giúp I2P dễ dùng hơn, từ đó giúp mạng lưới dễ phát triển hơn bằng cách làm cho phần mềm dễ tiếp cận hơn. Cả Java lẫn C++ đều gặp khó khăn khi sử dụng ngoài hệ sinh thái riêng của chúng, với C++ thường đòi hỏi các C binding viết tay mong manh và trong trường hợp của Java là sự phiền toái khi giao tiếp với một ứng dụng JVM từ một ứng dụng không chạy trên JVM.

Mặc dù ở nhiều phương diện tình huống này khá bình thường, tôi tin rằng có thể cải thiện để giúp I2P dễ tiếp cận hơn. Các ngôn ngữ khác có những giải pháp gọn gàng hơn cho các vấn đề này. Tất nhiên, chúng ta luôn nên cân nhắc và sử dụng các hướng dẫn hiện có dành cho các router Java và C++.

## sứ giả xuất hiện từ trong bóng tối

Hoàn toàn độc lập với nhóm của chúng tôi, một nhà phát triển tên là altonen đã phát triển một bản triển khai I2P bằng ngôn ngữ lập trình Rust có tên là emissary. Dù còn khá mới và Rust vẫn còn xa lạ với chúng tôi, dự án đầy hấp dẫn này rất hứa hẹn. Xin chúc mừng altonen vì đã tạo ra emissary; chúng tôi thực sự ấn tượng.

### Why Rust?

Lý do chính để sử dụng Rust về cơ bản cũng giống như lý do để dùng Java hoặc Go. Rust là một ngôn ngữ lập trình biên dịch có cơ chế quản lý bộ nhớ và một cộng đồng lớn, cực kỳ nhiệt huyết. Rust cũng cung cấp các tính năng nâng cao để tạo các bindings (liên kết) tới ngôn ngữ lập trình C, có thể dễ bảo trì hơn so với các ngôn ngữ khác, đồng thời vẫn thừa hưởng các đặc tính an toàn bộ nhớ mạnh mẽ của Rust.

### Do you want to get involved with emissary?

emissary được phát triển trên GitHub bởi altonen. Bạn có thể tìm kho mã tại: [altonen/emissary](https://github.com/altonen/emissary). Rust cũng đang thiếu các thư viện client SAMv3 toàn diện tương thích với các thư viện mạng phổ biến của Rust. Việc viết một thư viện SAMv3 là một điểm khởi đầu tuyệt vời.

## go-i2p is getting closer to completion

Trong khoảng 3 năm qua, tôi đã làm việc trên go-i2p, cố gắng biến một thư viện còn non thành một I2P router hoàn chỉnh viết bằng Go thuần, một ngôn ngữ an toàn bộ nhớ khác. Trong khoảng 6 tháng trở lại đây, nó đã được tái cấu trúc triệt để để cải thiện hiệu năng, độ tin cậy và khả năng bảo trì.

### Why Go?

Mặc dù Rust và Go có nhiều ưu điểm giống nhau, nhưng ở nhiều khía cạnh Go dễ học hơn rất nhiều. Trong nhiều năm qua, đã có những thư viện và ứng dụng rất tốt để sử dụng I2P bằng ngôn ngữ lập trình Go, bao gồm cả các triển khai đầy đủ nhất của các thư viện SAMv3.3. Nhưng nếu không có một router I2P mà chúng ta có thể quản lý tự động (chẳng hạn như một router nhúng), thì điều đó vẫn tạo ra rào cản cho người dùng. Mục tiêu của go-i2p là thu hẹp khoảng cách đó và loại bỏ mọi vướng mắc cho các nhà phát triển ứng dụng I2P đang làm việc với Go.

### Vì sao Rust?

go-i2p được phát triển trên Github, hiện chủ yếu bởi eyedeekay và mở cho các đóng góp từ cộng đồng tại [go-i2p](https://github.com/go-i2p/). Trong không gian tên này có nhiều dự án, chẳng hạn:

#### Router Libraries

Chúng tôi xây dựng các thư viện này để tạo ra các thư viện router I2P của chúng tôi. Chúng được phân tách thành nhiều kho lưu trữ chuyên biệt nhằm giúp việc rà soát trở nên dễ dàng hơn và để chúng hữu ích cho những người khác muốn xây dựng các router I2P thử nghiệm, tùy biến.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

À, có một dự án đang tạm ngưng để viết một [I2P router in C#](https://github.com/PeterZander/i2p-cs) nếu bạn muốn chạy I2P trên XBox. Nghe cũng khá thú vị đấy. Nếu điều đó cũng không hợp ý bạn, bạn có thể làm như altonen đã làm và phát triển một router hoàn toàn mới.

### Bạn có muốn tham gia vào emissary không?

Bạn có thể viết một I2P router vì bất kỳ lý do nào — đây là một mạng tự do — nhưng sẽ hữu ích nếu bạn biết vì sao. Bạn có một cộng đồng muốn trao quyền, một công cụ bạn cho rằng phù hợp với I2P, hoặc một chiến lược bạn muốn thử nghiệm không? Hãy xác định mục tiêu của bạn để biết cần bắt đầu từ đâu và trạng thái "hoàn thành" sẽ trông như thế nào.

### Decide what language you want to do it in and why

Sau đây là một số lý do bạn có thể chọn một ngôn ngữ:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Tuy nhiên, đây là một số lý do vì sao bạn có thể không chọn những ngôn ngữ đó:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Có hàng trăm ngôn ngữ lập trình và chúng tôi hoan nghênh các thư viện I2P và routers được duy trì trong tất cả các ngôn ngữ đó. Hãy lựa chọn các đánh đổi của bạn một cách sáng suốt và bắt đầu.

## go-i2p đang tiến gần đến việc hoàn thành

Dù bạn muốn làm việc bằng Rust, Go, Java, C++ hay ngôn ngữ khác, hãy liên hệ với chúng tôi tại #i2p-dev trên Irc2P. Hãy bắt đầu từ đó, và chúng tôi sẽ hướng dẫn bạn tham gia các kênh dành riêng cho router. Chúng tôi cũng có mặt trên ramble.i2p tại f/i2p, trên reddit tại r/i2p, và trên GitHub và git.idk.i2p. Chúng tôi mong sớm nhận được tin từ bạn.
