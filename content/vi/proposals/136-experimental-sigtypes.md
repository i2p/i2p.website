---
title: "Hỗ trợ Floodfill cho Các Loại Chữ Ký Thử Nghiệm"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Tổng quan

Đối với các loại chữ ký trong phạm vi thử nghiệm (65280-65534), floodfills nên chấp nhận lưu trữ netdb mà không kiểm tra chữ ký.

Điều này sẽ hỗ trợ thử nghiệm các loại chữ ký mới.


## Động lực

Đề xuất GOST 134 đã tiết lộ hai vấn đề với phạm vi loại chữ ký thử nghiệm chưa được sử dụng trước đây.

Thứ nhất, vì các loại chữ ký trong phạm vi thử nghiệm không thể được dành riêng, chúng có thể được sử dụng cho nhiều loại chữ ký cùng lúc.

Thứ hai, trừ khi thông tin router hay lease set với một loại chữ ký thử nghiệm có thể được lưu trữ ở floodfill, việc thử nghiệm hoàn toàn hay sử dụng thử nghiệm loại chữ ký mới rất khó khăn.


## Thiết kế

Floodfills nên chấp nhận, và lưu truyền, các lưu trữ LS với các loại chữ ký trong phạm vi thử nghiệm, mà không kiểm tra chữ ký. Hỗ trợ cho lưu trữ RI còn chưa rõ, và có thể có thêm các vấn đề an ninh.


## Đặc tả


Đối với các loại chữ ký trong phạm vi thử nghiệm, một floodfill nên chấp nhận và lưu truyền lưu trữ netdb mà không kiểm tra chữ ký.

Để ngăn chặn giả mạo router và đích đến không thử nghiệm, một floodfill không bao giờ nên chấp nhận lưu trữ của loại chữ ký thử nghiệm mà có đụng độ hash với một mục nhập netdb hiện có của loại chữ ký khác. Điều này ngăn chặn việc chiếm quyền kiểm soát của một mục nhập netdb trước đó.

Ngoài ra, một floodfill nên ghi đè một mục nhập netdb thử nghiệm bằng một lưu trữ của loại chữ ký không thử nghiệm mà có đụng độ hash, để ngăn chặn việc chiếm quyền kiểm soát của một hash trước đó không có.

Floodfills nên giả định độ dài khóa công khai chữ ký là 128, hoặc suy luận nó từ độ dài chứng chỉ khóa, nếu dài hơn. Một số triển khai có thể không hỗ trợ độ dài lớn hơn trừ khi loại chữ ký được dành riêng không chính thức.


## Di chuyển

Khi tính năng này được hỗ trợ, trong một phiên bản router đã biết, các mục nhập netdb loại chữ ký thử nghiệm có thể được lưu trữ đến floodfills của phiên bản đó hoặc cao hơn.

Nếu một số triển khai router không hỗ trợ tính năng này, lưu trữ netdb sẽ thất bại, nhưng điều đó giống như hiện tại.


## Vấn đề

Có thể có thêm các vấn đề an ninh, cần được nghiên cứu (xem đề xuất 137)

Một số triển khai có thể không hỗ trợ độ dài khóa lớn hơn 128, như đã mô tả ở trên. Ngoài ra, có thể cần thiết phải thực thi một tối đa là 128 (nói cách khác, không có dữ liệu khóa thừa trong chứng chỉ khóa), để giảm khả năng của kẻ tấn công tạo ra đụng độ hash.

Các vấn đề tương tự sẽ cần được giải quyết với các loại mã hóa không bằng không, điều này chưa được đề xuất chính thức.


## Ghi chú

Lưu trữ NetDB của các loại chữ ký không rõ không nằm trong phạm vi thử nghiệm sẽ tiếp tục bị từ chối bởi floodfills, vì chữ ký không thể được xác minh.


