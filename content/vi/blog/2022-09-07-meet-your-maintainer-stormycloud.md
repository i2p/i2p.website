---
title: "Gặp gỡ người bảo trì của bạn: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Một cuộc phỏng vấn với đội ngũ duy trì Outproxy StormyCloud (proxy ra)"
categories: ["general"]
---

## Một cuộc trò chuyện với StormyCloud Inc.

Với [bản phát hành I2P Java](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release) mới nhất, outproxy (proxy thoát) hiện có, false.i2p, đã được thay thế bằng StormyCloud outproxy mới cho các cài đặt I2P mới. Đối với những người đang cập nhật router, việc chuyển sang dịch vụ Stormycloud có thể được thực hiện nhanh chóng.

Trong Hidden Services Manager, hãy đổi cả Outproxies và SSL Outproxies thành exit.stormycloud.i2p và nhấp vào nút lưu ở cuối trang.

## StormyCloud Inc là ai?

**Sứ mệnh của StormyCloud Inc.**

Bảo vệ quyền tiếp cận Internet như một quyền con người phổ quát. Bằng cách đó, nhóm bảo vệ quyền riêng tư điện tử của người dùng và xây dựng cộng đồng bằng cách thúc đẩy việc tiếp cận thông tin không bị hạn chế, qua đó tạo điều kiện cho tự do trao đổi ý tưởng xuyên biên giới. Điều này là thiết yếu vì Internet là công cụ mạnh mẽ nhất hiện có để mang lại tác động tích cực cho thế giới.

**Tuyên bố tầm nhìn**

Trở thành người tiên phong trong việc cung cấp Internet tự do và mở cho mọi người trong vũ trụ vì quyền truy cập Internet là một quyền cơ bản của con người ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Tôi gặp Dustin để chào hỏi, và để bàn thêm về quyền riêng tư, nhu cầu đối với các dịch vụ như StormyCloud, và điều gì đã thu hút công ty đến với I2P.

**Nguồn cảm hứng đằng sau việc thành lập StormyCloud là gì?**

Vào cuối năm 2021, tôi đang ở trên subreddit /r/tor. Có một người đã trả lời trong một chủ đề về cách sử dụng Tor, kể rằng họ dựa vào Tor để giữ liên lạc với gia đình. Gia đình họ sống ở Hoa Kỳ, nhưng vào thời điểm đó họ đang sống ở một quốc gia nơi quyền truy cập Internet bị hạn chế rất nghiêm ngặt. Họ cần hết sức thận trọng về việc mình giao tiếp với ai và nói những gì. Vì những lý do đó, họ dựa vào Tor. Tôi nghĩ về việc làm sao tôi có thể giao tiếp với mọi người mà không sợ hãi hay bị hạn chế, và rằng điều đó nên như vậy đối với tất cả mọi người.

Mục tiêu của StormyCloud là giúp càng nhiều người càng tốt thực hiện điều đó.

**Một số thách thức trong việc đưa StormyCloud vào hoạt động là gì?**

Chi phí — đắt khủng khiếp. Chúng tôi chọn phương án trung tâm dữ liệu vì quy mô những gì chúng tôi đang làm không thể thực hiện trên một mạng gia đình. Có chi phí thiết bị và chi phí hosting định kỳ.

Về việc thành lập tổ chức phi lợi nhuận, chúng tôi đi theo con đường của Emerald Onion và tận dụng một số tài liệu cũng như các bài học kinh nghiệm của họ. Cộng đồng Tor có rất nhiều tài nguyên sẵn có và rất hữu ích.

**Phản hồi đối với các dịch vụ của bạn đến nay như thế nào?**

Vào tháng 7, chúng tôi đã phục vụ 1,5 tỷ yêu cầu DNS trên tất cả các dịch vụ của mình. Mọi người đánh giá cao việc không có hoạt động ghi log nào. Đơn giản là không có dữ liệu, và mọi người thích điều đó.

**outproxy là gì?**

Một outproxy (proxy ra ngoài) tương tự các nút thoát của Tor; nó cho phép lưu lượng clearnet (lưu lượng internet thông thường) được chuyển tiếp qua mạng I2P. Nói cách khác, nó cho phép người dùng I2P truy cập internet một cách an toàn thông qua mạng I2P.

**Outproxy I2P (proxy đi ra khỏi I2P) của StormyCloud có gì đặc biệt?**

Trước hết, chúng tôi là multi-homed (kết nối tới nhiều mạng/ISP), nghĩa là chúng tôi có nhiều máy chủ phục vụ lưu lượng outproxy. Điều này bảo đảm dịch vụ luôn sẵn sàng cho cộng đồng. Toàn bộ log (nhật ký) trên các máy chủ của chúng tôi được xóa sạch cứ mỗi 15 phút. Điều này bảo đảm rằng cả cơ quan thực thi pháp luật lẫn chính chúng tôi đều không thể truy cập bất kỳ dữ liệu nào. Chúng tôi hỗ trợ truy cập các liên kết .onion của Tor thông qua outproxy, và outproxy của chúng tôi khá nhanh.

**Bạn định nghĩa quyền riêng tư như thế nào? Bạn thấy những vấn đề nào với tình trạng can thiệp quá mức và việc xử lý dữ liệu?**

Quyền riêng tư là trạng thái không bị truy cập trái phép. Tính minh bạch là điều quan trọng, chẳng hạn cơ chế đồng ý tham gia (opt-in) — điển hình là các yêu cầu của GDPR.

Có những công ty lớn đang tích trữ dữ liệu, và dữ liệu này đang được sử dụng để [truy cập dữ liệu vị trí mà không cần lệnh](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). Có sự can thiệp quá mức của các công ty công nghệ vào những gì mọi người nghĩ là, và lẽ ra phải là, riêng tư, như ảnh hoặc tin nhắn.

Điều quan trọng là tiếp tục làm công tác nâng cao nhận thức về cách giữ an toàn cho việc giao tiếp của bạn, và về những công cụ hoặc ứng dụng sẽ giúp một người thực hiện điều đó. Cách chúng ta tương tác với tất cả các thông tin ngoài kia cũng quan trọng. Chúng ta cần tin nhưng phải kiểm chứng.

**I2P phù hợp như thế nào với Tuyên bố Sứ mệnh và Tầm nhìn của StormyCloud?**

I2P là một dự án mã nguồn mở, và những gì nó mang lại phù hợp với sứ mệnh của StormyCloud Inc. I2P cung cấp một lớp quyền riêng tư và bảo vệ cho lưu lượng và giao tiếp, và dự án tin rằng mọi người đều có quyền riêng tư.

Chúng tôi biết đến I2P vào đầu năm 2022 khi nói chuyện với những người trong cộng đồng Tor và thích những gì dự án đang làm. Nó có vẻ giống Tor.

Trong quá trình giới thiệu I2P và các khả năng của nó, chúng tôi nhận thấy cần có một outproxy đáng tin cậy. Chúng tôi đã nhận được sự hỗ trợ rất lớn từ những người trong cộng đồng I2P để tạo lập và bắt đầu cung cấp dịch vụ outproxy.

**Kết luận**

Nhu cầu nâng cao nhận thức về tình trạng giám sát những gì lẽ ra phải riêng tư trong đời sống trực tuyến của chúng ta vẫn tiếp diễn. Việc thu thập bất kỳ dữ liệu nào phải dựa trên sự đồng thuận, và quyền riêng tư phải được mặc nhiên bảo đảm.

Khi chúng ta không thể tin tưởng rằng lưu lượng mạng hoặc liên lạc của mình sẽ không bị giám sát mà không có sự đồng ý, thì rất may là chúng ta có quyền truy cập vào các mạng mà theo thiết kế sẽ ẩn danh hóa lưu lượng và che giấu vị trí của chúng ta.

Cảm ơn StormyCloud và tất cả những ai cung cấp outproxy (proxy ra ngoài) hoặc các nút cho Tor và I2P để mọi người có thể truy cập internet an toàn hơn khi cần. Tôi mong sẽ có nhiều người hơn kết nối các khả năng của những mạng bổ trợ lẫn nhau này để tạo ra một hệ sinh thái quyền riêng tư mạnh mẽ hơn cho tất cả mọi người.

Tìm hiểu thêm về các dịch vụ của StormyCloud Inc. tại [https://stormycloud.org/](https://stormycloud.org/) và ủng hộ hoạt động của họ bằng cách quyên góp tại [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
