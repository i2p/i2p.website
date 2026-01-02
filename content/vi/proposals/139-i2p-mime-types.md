---
title: "Loại MIME I2P"
number: "139"
author: "zzz"
created: "2017-05-16"
lastupdated: "2017-05-16"
status: "Open"
thread: "http://zzz.i2p/topics/1957"
toc: true
---

## Tổng quan

Định nghĩa các loại MIME cho các định dạng tệp I2P phổ biến.
Bao gồm các định nghĩa trong các gói Debian.
Cung cấp một bộ xử lý cho loại .su3, và có thể là các loại khác.


## Động cơ

Để làm cho việc cài đặt lại và cài đặt plugin dễ dàng hơn khi tải xuống bằng trình duyệt,
chúng ta cần một loại MIME và bộ xử lý cho các tệp .su3.

Nhân cơ hội này, sau khi học cách viết tệp định nghĩa MIME,
theo tiêu chuẩn freedesktop.org, chúng ta có thể thêm định nghĩa cho các loại tệp I2P phổ biến khác.
Mặc dù ít hữu ích hơn cho các tệp không thường xuyên được tải xuống, chẳng hạn như
cơ sở dữ liệu blockfile addressbook (hostsdb.blockfile), các định nghĩa này sẽ
giúp các tệp được nhận diện và biểu tượng hóa tốt hơn khi sử dụng chương trình xem thư mục đồ họa
như "nautilus" trên Ubuntu.

Bằng cách chuẩn hóa các loại MIME, mỗi triển khai router có thể viết bộ xử lý
phù hợp, và tệp định nghĩa MIME có thể được chia sẻ bởi tất cả các triển khai.


## Thiết kế

Viết một tệp nguồn XML theo tiêu chuẩn freedesktop.org và bao gồm trong
các gói Debian. Tệp này là "debian/(package).sharedmimeinfo".

Tất cả các loại MIME I2P sẽ bắt đầu với "application/x-i2p-", ngoại trừ jrobin rrd.

Các bộ xử lý cho các loại MIME này là đặc thù cho ứng dụng và sẽ không
được xác định ở đây.

Chúng ta cũng sẽ bao gồm các định nghĩa với Jetty, và bao gồm chúng với
phần mềm cài lại hoặc hướng dẫn.


## Đặc tả

.blockfile 		application/x-i2p-blockfile

.config 		application/x-i2p-config

.dat	 		application/x-i2p-privkey

.dat	 		application/x-i2p-dht

=.dat	 		application/x-i2p-routerinfo

.ht	 		application/x-i2p-errorpage

.info	 		application/x-i2p-routerinfo

.jrb	 		application/x-jrobin-rrd

.su2			application/x-i2p-update

.su3	(tổng quát)	application/x-i2p-su3

.su3	(cập nhật router)	application/x-i2p-su3-update

.su3	(plugin)	application/x-i2p-su3-plugin

.su3	(cài lại)	application/x-i2p-su3-reseed

.su3	(tin tức)		application/x-i2p-su3-news

.su3	(danh sách chặn)	application/x-i2p-su3-blocklist

.sud			application/x-i2p-update

.syndie	 		application/x-i2p-syndie

=.txt.gz 		application/x-i2p-peerprofile

.xpi2p	 		application/x-i2p-plugin


## Ghi chú

Không phải tất cả các định dạng tệp được liệt kê ở trên đều được sử dụng bởi các triển khai router không phải Java;
một số có thể thậm chí không được định nghĩa rõ ràng. Tuy nhiên, tài liệu hóa chúng ở đây
có thể giúp tạo sự nhất quán giữa các triển khai trong tương lai.

Một số hậu tố tệp như ".config", ".dat" và ".info" có thể trùng lặp với
các loại MIME khác. Chúng có thể được phân biệt với dữ liệu bổ sung như
tên tệp đầy đủ, mẫu tên tệp, hoặc số ma thuật.
Xem tệp dự thảo i2p.sharedmimeinfo trong chủ đề zzz.i2p để biết ví dụ.

Các loại quan trọng là các loại .su3, và những loại đó đều có
một hậu tố duy nhất và định nghĩa số ma thuật mạnh mẽ.


## Di cư

Không áp dụng.
