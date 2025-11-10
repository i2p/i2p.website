---
title: "I2P không bị ảnh hưởng bởi lỗ hổng bảo mật log4j"
date: 2021-12-11
author: "idk, zzz"
description: "I2P không sử dụng log4j và do đó không bị ảnh hưởng bởi CVE-2021-44228"
categories: ["security"]
---

I2P không bị ảnh hưởng bởi lỗ hổng 0-day log4j được công bố ngày hôm qua, CVE-2021-44228. I2P không sử dụng log4j để ghi nhật ký, tuy nhiên chúng tôi cũng cần rà soát các phụ thuộc của mình về việc sử dụng log4j, đặc biệt là Jetty. Việc rà soát này không phát hiện bất kỳ lỗ hổng nào.

Việc kiểm tra tất cả các plugin (phần bổ trợ) của chúng tôi cũng rất quan trọng. Các plugin có thể tích hợp các hệ thống ghi log riêng của chúng, bao gồm cả log4j. Chúng tôi nhận thấy rằng phần lớn plugin cũng không sử dụng log4j, và những plugin có sử dụng thì không dùng phiên bản log4j có lỗ hổng.

Chúng tôi chưa phát hiện bất kỳ thư viện phụ thuộc, plugin hoặc ứng dụng nào có lỗ hổng bảo mật.

Chúng tôi đóng gói kèm một tệp log4j.properties với jetty cho các plugin tích hợp log4j. Tệp này chỉ ảnh hưởng đến các plugin sử dụng log4j để ghi nhật ký nội bộ. Chúng tôi đã đưa biện pháp giảm thiểu được khuyến nghị vào tệp log4j.properties. Các plugin kích hoạt log4j sẽ chạy với tính năng có lỗ hổng bị vô hiệu hóa. Vì chúng tôi không tìm thấy bất kỳ việc sử dụng log4j 2.x ở bất kỳ đâu, chúng tôi không có kế hoạch phát hành khẩn cấp vào thời điểm này.
