---
title: "Cuộc họp các nhà phát triển I2P - 03 tháng 9 năm 2019"
date: 2019-09-03
author: "zzz"
description: "Biên bản cuộc họp phát triển I2P ngày 03 tháng 9 năm 2019."
categories: ["meeting"]
---

## Quick recap

<p class="attendees-inline"><strong>Present:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Nhật ký cuộc họp

<div class="irc-log">                Lưu ý: các dòng của sadie không xuất hiện trong cuộc họp, được dán bên dưới.

20:00:00 &lt;zzz&gt; 0) Chào 20:00:00 &lt;zzz&gt; 1) Tình trạng phát hành 0.9.42 (zzz) 20:00:00 &lt;zzz&gt; 2) Tình trạng dự án I2P Browser "labs" (sadie, meeh) 20:00:00 &lt;zzz&gt; 3) Các trường hợp sử dụng Outproxy / tình trạng (sadie) 20:00:00 &lt;zzz&gt; 4) Tình trạng phát triển 0.9.43 (zzz) 20:00:00 &lt;zzz&gt; 5) Tình trạng các đề xuất (zzz) 20:00:00 &lt;zzz&gt; 6) Scrum trạng thái (zlatinb)
20:00:04 &lt;zzz&gt; 0) Chào
20:00:06 &lt;zzz&gt; chào
20:00:17 &lt;zlatinb&gt; chào
20:00:30 &lt;zzz&gt; 1) Tình trạng phát hành 0.9.42 (zzz)
20:00:48 &lt;zzz&gt; đợt phát hành tuần trước diễn ra khá suôn sẻ
20:00:56 &lt;zzz&gt; chỉ còn một vài việc tồn đọng
20:01:27 &lt;zzz&gt; khôi phục github bridge hoạt động trở lại (nextloop), gói debian sid (mhatta), và thư viện client Android mà chúng ta đã quên cho bản 41 (meeh)
20:01:37 &lt;zzz&gt; nextloop, meeh, các bạn có ETAs (thời hạn ước tính) cho những hạng mục đó không?
20:03:06 &lt;zzz&gt; còn gì nữa cho mục 1) không?
20:04:02 &lt;zzz&gt; 2) Tình trạng dự án I2P Browser "labs" (sadie, meeh)
20:04:25 &lt;zzz&gt; sadie, meeh, tình trạng ra sao, và mốc tiếp theo là gì?          &lt;sadie&gt; Beta 5 dự kiến ra mắt vào thứ Sáu, nhưng đã có một số vấn đề. Có vẻ một vài bản đã sẵn sàng https://i2bbparts.meeh.no/i2p-browser/ nhưng tôi thực sự cần nghe từ meeh về hạn chót tiếp theo cho việc này          &lt;sadie&gt; Trang Lab sẽ hoạt động trước cuối tuần này. Mốc tiếp theo của Browser sẽ là thảo luận các yêu cầu của bảng điều khiển cho phát hành beta 6
20:05:51 &lt;zzz&gt; còn gì nữa cho mục 2) không?
20:06:43 &lt;zzz&gt; 3) Các trường hợp sử dụng Outproxy / tình trạng (sadie)
20:06:57 &lt;zzz&gt; sadie, tình trạng ra sao, và mốc tiếp theo là gì?          &lt;sadie&gt; Ai cũng có thể theo dõi biên bản họp của chúng tôi trên ticket 2472. Chúng tôi đã quyết định các trạng thái của các trường hợp sử dụng và có một danh sách yêu cầu. Mốc tiếp theo sẽ là yêu cầu người dùng cho một trường hợp sử dụng Friends and Family, cũng như các yêu cầu phát triển cho Friends and Familiy và trường hợp sử dụng General để xem chúng có chồng lấn ở đâu
20:08:05 &lt;zzz&gt; còn gì nữa cho mục 3) không?
20:08:19 &lt;eyedeekay&gt; Xin lỗi tôi đến muộn
20:09:01 &lt;zzz&gt; 4) Tình trạng phát triển 0.9.43 (zzz)
20:09:21 &lt;zzz&gt; chúng tôi vừa bắt đầu chu kỳ 43, dự kiến phát hành trong khoảng 7 tuần nữa
20:09:40 &lt;zzz&gt; chúng tôi đã cập nhật lộ trình trên trang web nhưng sẽ bổ sung thêm một số hạng mục
20:10:06 &lt;zzz&gt; tôi đã sửa một số lỗi IPv6 và tăng tốc xử lý AES cho tunnel
20:10:30 &lt;zzz&gt; sắp tới tôi sẽ chuyển sự chú ý sang thông điệp I2CP về thông tin blinding (làm mù) mới
20:10:59 &lt;zzz&gt; eyedeekay, zlatinb, các bạn có gì bổ sung về .43 không?
20:11:46 &lt;eyedeekay&gt; Không, tôi không nghĩ vậy
20:12:02 &lt;zlatinb&gt; có lẽ thêm vài thứ về mạng thử nghiệm
20:12:32 &lt;zzz&gt; vâng, chúng ta còn một vài jogger tickets cần xem, liên quan đến SSU
20:12:48 &lt;zzz&gt; còn gì nữa cho mục 4) không?
20:14:00 &lt;zzz&gt; 5) Tình trạng các đề xuất (zzz)
20:14:20 &lt;zzz&gt; trọng tâm chính của chúng tôi là đề xuất mã hóa mới 144, rất phức tạp
20:14:48 &lt;zzz&gt; chúng tôi đã đạt một số tiến triển tốt trong vài tuần gần đây và đã có một số cập nhật lớn cho chính đề xuất đó
20:15:35 &lt;zzz&gt; còn một vài việc dọn dẹp và lỗ hổng cần lấp đầy, nhưng tôi hy vọng nó đã đủ ổn để chúng ta có thể bắt đầu viết một số hiện thực kiểm thử đơn vị sớm, có thể vào cuối tháng
20:16:17 &lt;zzz&gt; ngoài ra, thông điệp thông tin blinding cho đề xuất 123 (LS2 được mã hóa) sẽ được xem xét lại sau khi tôi bắt đầu mã hóa nó trong tuần tới
20:16:52 &lt;zzz&gt; cũng sắp tới, chúng tôi kỳ vọng có bản cập nhật về đề xuất 152 (thông điệp xây dựng tunnel) từ chisana
20:17:27 &lt;zzz&gt; chúng tôi đã hoàn tất đề xuất 147 (ngăn chặn xuyên mạng) vào tháng trước và cả i2p lẫn i2pd đều đã có mã cho việc đó trong bản phát hành .42
20:18:23 &lt;zzz&gt; vì vậy mọi thứ đang tiến lên; dù 144 có vẻ chậm và đáng ngại, nó vẫn đang tiến triển tốt
20:18:27 &lt;zzz&gt; còn gì nữa cho mục 5) không?
20:20:00 &lt;zzz&gt; 6) Scrum trạng thái (zlatinb)
20:20:05 &lt;zzz&gt; mời zlatinb
20:20:42 &lt;zlatinb&gt; Chào, vui lòng nói ngắn gọn: 1) bạn đã làm gì kể từ phiên scrum trước 2) bạn dự định làm gì trong tháng tới 3) bạn có vướng mắc nào hoặc cần giúp đỡ không. Ghi EOT khi xong
20:21:23 &lt;zlatinb&gt; tôi: 1) Nhiều thử nghiệm trên mạng thử nghiệm để tăng tốc truyền tải khối lượng lớn 2) thêm công việc trên mạng thử nghiệm trên máy chủ/mạng hy vọng lớn hơn 3) không có vướng mắc EOT
20:22:15 &lt;zzz&gt; 1) sửa lỗi, thay đổi tách cấu hình, phát hành .42, các đề xuất, workshop DEFCON (xem báo cáo chuyến đi của tôi trên i2pforum và trang web của chúng tôi)
20:23:56 &lt;zzz&gt; 2) sửa lỗi, đề xuất 144, thông điệp thông tin blinding, tăng tốc, hỗ trợ nghiên cứu outproxy, sửa trình hướng dẫn SSL bị hỏng do việc tách cấu hình
20:24:20 &lt;zzz&gt; sửa thêm về IPv6
20:24:38 &lt;zzz&gt; 3) không có vướng mắc EOT
20:24:50 &lt;eyedeekay&gt; 1) Kể từ phiên scrum trước tôi đã làm sửa lỗi, trang web, làm việc trên đề xuất outproxy, và các việc liên quan đến i2ptunnels. 2) Tiếp tục tổ chức lại và cải thiện cách trình bày của trang web. Tiếp tục thúc đẩy đề xuất outproxy 3) không có vướng mắc EOT          &lt;sadie&gt; 1) Tham dự FOCI, nghiên cứu các phương án tài trợ, gặp gỡ các nhà tài trợ tiềm năng, có một cuộc họp với Tails (bao gồm cả Mhatta), làm việc về thương hiệu I2P Browser, cập nhật trang web với IDK, thực hiện một vài thay đổi nhỏ cho bảng điều khiển cho bản phát hành vừa rồi          &lt;sadie&gt; 2) tháng tới tôi sẽ làm hồ sơ tài trợ, cải tiến bảng điều khiển và trang web, trình hướng dẫn thiết lập, tham dự Our Networks ở Toronto, thúc đẩy I2P Browser và nghiên cứu OutProxy          &lt;sadie&gt; 3) không có vướng mắc EOT
20:25:29 &lt;zlatinb&gt; scrum.setTimeout( 60 * 1000 );
20:27:04 &lt;zzz&gt; được, hết thời gian
20:27:10 &lt;zlatinb&gt; ScrumTimeoutException
20:27:41 &lt;zzz&gt; gọi lần cuối cho sadie meeh nextloop quay lại các mục 1)-3)
20:27:52 &lt;zzz&gt; còn chủ đề nào khác cho cuộc họp không?
20:28:47 * zzz chộp lấy baffer
20:30:00 * zzz ***bafs*** cuộc họp kết thúc </div>
