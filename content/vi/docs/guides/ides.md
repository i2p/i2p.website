---
title: "Sử dụng IDE với I2P"
description: "Thiết lập Eclipse và NetBeans để phát triển I2P với Gradle và các tệp dự án đi kèm"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: tài liệu
reviewStatus: "needs-review"
---

<p> Nhánh phát triển chính của I2P (<code>i2p.i2p</code>) đã được thiết lập để giúp các nhà phát triển dễ dàng cài đặt hai IDE thường được sử dụng cho phát triển Java: Eclipse và NetBeans. </p>

<h2>Eclipse</h2>

<p> Các nhánh phát triển chính của I2P (<code>i2p.i2p</code> và các nhánh từ đó) chứa <code>build.gradle</code> để cho phép nhánh được thiết lập dễ dàng trong Eclipse. </p>

<ol> <li> Đảm bảo bạn có phiên bản Eclipse gần đây. Bất kỳ phiên bản nào mới hơn 2017 đều có thể dùng được. </li> <li> Check out nhánh I2P vào một thư mục nào đó (ví dụ: <code>$HOME/dev/i2p.i2p</code>). </li> <li> Chọn "File → Import..." và sau đó trong mục "Gradle" chọn "Existing Gradle Project". </li> <li> Tại "Project root directory:" chọn thư mục mà nhánh I2P đã được check out vào. </li> <li> Trong hộp thoại "Import Options", chọn "Gradle Wrapper" và nhấn Continue. </li> <li> Trong hộp thoại "Import Preview" bạn có thể xem lại cấu trúc dự án. Nhiều dự án sẽ xuất hiện trong "i2p.i2p". Nhấn "Finish". </li> <li> Xong! Workspace của bạn giờ đây sẽ chứa tất cả các dự án trong nhánh I2P, và các build dependencies của chúng sẽ được thiết lập đúng cách. </li> </ol>

<h2>NetBeans</h2>

<p> Các nhánh phát triển chính của I2P (<code>i2p.i2p</code> và các nhánh từ đó) chứa các tệp dự án NetBeans. </p>

<!-- Giữ nội dung tối thiểu và gần với bản gốc; sẽ cập nhật sau. -->
