---
title: "Thư Mục Dịch Vụ"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Bị Từ Chối"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Tổng Quan

Đề xuất này là cho một giao thức mà các ứng dụng có thể sử dụng để đăng ký và tra cứu các dịch vụ trong một thư mục.


## Động Lực

Cách đơn giản nhất để hỗ trợ onioncat là với một thư mục dịch vụ.

Điều này tương tự với một đề xuất của Sponge đã từng có trên IRC. Tôi không nghĩ rằng anh ấy đã viết nó ra, nhưng ý tưởng của anh ấy là đưa nó vào netDb. Tôi không ủng hộ điều đó, nhưng cuộc thảo luận về phương pháp tốt nhất để truy cập vào thư mục (các tra cứu netDb, DNS-over-i2p, HTTP, hosts.txt, v.v.) tôi sẽ để dành cho một ngày khác.

Tôi có thể hack điều này khá nhanh chóng bằng cách sử dụng HTTP và bộ sưu tập các script perl mà tôi sử dụng cho biểu mẫu thêm khóa.


## Đặc Tả Kỹ Thuật

Đây là cách một ứng dụng sẽ giao tiếp với thư mục:

ĐĂNG KÝ
  - DestKey
  - Danh sách các cặp Giao Thức/Dịch Vụ:

    - Giao Thức (tùy chọn, mặc định: HTTP)
    - Dịch Vụ (tùy chọn, mặc định: trang web)
    - ID (tùy chọn, mặc định: không có)

  - Tên Máy Chủ (tùy chọn)
  - Thời Gian Hết Hạn (mặc định: 1 ngày? 0 để xóa)
  - Chữ Ký (sử dụng khóa riêng cho điểm đích)

  Trả về: thành công hoặc thất bại

  Các cập nhật được phép

TRA CỨU
  - Băm hoặc khóa (tùy chọn). MỘT trong số:

    - Băm một phần 80-bit
    - Băm đầy đủ 256-bit
    - khóa điểm đến đầy đủ

  - Cặp giao thức/dịch vụ (tùy chọn)

  Trả về: thành công, thất bại, hoặc (đối với 80-bit) xung đột.
  Nếu thành công, trả về mô tả đã ký ở trên.
