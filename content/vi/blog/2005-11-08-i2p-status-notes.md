---
title: "Ghi chú trạng thái I2P cho ngày 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Cập nhật hàng tuần về độ ổn định của 0.6.1.4, lộ trình tối ưu hóa hiệu năng, phát hành I2Phex 0.1.1.35, phát triển client BT I2P-Rufus, tiến triển của I2PSnarkGUI, và đại tu UI (giao diện người dùng) của Syndie"
categories: ["status"]
---

Chào mọi người, lại đến thứ Ba rồi.

* Index

1) Trạng thái mạng / lộ trình ngắn hạn 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

0.6.1.4 vẫn có vẻ khá ổn định, mặc dù đã có một số bản sửa lỗi trong CVS kể từ đó. Tôi cũng đã thêm một số tối ưu hóa cho SSU để truyền dữ liệu hiệu quả hơn, điều mà tôi hy vọng sẽ tạo ra tác động đáng chú ý đối với mạng khi nó được triển khai rộng rãi. Tuy nhiên, hiện tôi tạm hoãn 0.6.1.5, vì còn một vài thứ khác tôi muốn đưa vào bản phát hành tiếp theo. Kế hoạch hiện tại là phát hành nó vào cuối tuần này, vì vậy hãy chú ý theo dõi những tin tức mới nhất.

Bản phát hành 0.6.2 sẽ bao gồm nhiều cải tiến quan trọng để đối phó với những kẻ tấn công còn mạnh hơn, nhưng có một điều nó sẽ không ảnh hưởng tới: hiệu năng. Mặc dù ẩn danh chắc chắn là mục tiêu cốt lõi của I2P, nếu thông lượng thấp và độ trễ cao, chúng ta sẽ chẳng có người dùng nào. Vì vậy, kế hoạch của tôi là nâng hiệu năng lên mức cần thiết trước khi tiến hành triển khai các chiến lược sắp xếp peer (nút ngang hàng) của 0.6.2 và các kỹ thuật tạo tunnel mới.

* 2) I2Phex

Gần đây mảng I2Phex cũng rất sôi động, với bản phát hành 0.1.1.35 mới [1]. Ngoài ra còn có thêm các thay đổi trong CVS (cảm ơn Legion!), nên tôi sẽ không ngạc nhiên nếu thấy 0.1.1.36 được phát hành trong tuần này.

Cũng đã có một số tiến triển tốt ở mảng gwebcache (xem http://awup.i2p/), mặc dù theo như tôi biết thì vẫn chưa có ai bắt đầu làm việc để sửa đổi I2Phex nhằm sử dụng một gwebcache hỗ trợ I2P (quan tâm chứ? cho tôi biết nhé!)

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Nghe đồn defnax và Rawn đang hack ứng dụng khách BT Rufus, hợp nhất một số mã nguồn liên quan đến I2P từ I2P-BT. Tôi không rõ tình trạng hiện tại của bản port, nhưng nghe có vẻ nó sẽ có vài tính năng thú vị. Tôi chắc rằng khi có thêm thông tin để chia sẻ, chúng ta sẽ được biết thêm.

* 4) I2PSnarkGUI

Một tin đồn khác đang lan truyền là Markus đang mày mò phát triển một GUI C# (giao diện đồ họa người dùng) mới... ảnh chụp màn hình trên PlanetPeer trông khá ấn tượng [2]. Vẫn có kế hoạch cho một giao diện web không phụ thuộc nền tảng, nhưng nó trông khá ổn. Tôi chắc rằng chúng ta sẽ còn nghe thêm từ Markus khi GUI tiến triển.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Cũng đã có một số thảo luận về việc đại tu giao diện người dùng của Syndie [3], và tôi kỳ vọng chúng ta sẽ sớm thấy một số tiến triển ở mảng này. dust cũng đang miệt mài với Sucker, bổ sung hỗ trợ tốt hơn cho việc thu thập thêm nhiều nguồn cấp RSS/Atom vào Syndie, cũng như một số cải tiến cho chính SML.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Rất nhiều việc đang diễn ra, như thường lệ. Hãy ghé qua #i2p trong vài phút nữa để tham gia cuộc họp dev hàng tuần của chúng tôi.

=jr
