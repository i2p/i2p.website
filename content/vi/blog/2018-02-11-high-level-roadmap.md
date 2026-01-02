---
title: "Lộ trình tổng quan cho năm 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 sẽ là năm của các giao thức mới, các hợp tác mới, và một trọng tâm được tinh chỉnh hơn."
categories: ["roadmap"]
---

Một trong nhiều điều chúng tôi đã thảo luận tại 34C3 là chúng tôi nên tập trung vào điều gì trong năm tới. Cụ thể là, chúng tôi muốn có một lộ trình làm rõ những việc chúng tôi muốn bảo đảm sẽ hoàn thành, so với những thứ nếu có thì sẽ rất tốt, và có thể giúp người mới tham gia vào một trong hai nhóm đó. Dưới đây là những gì chúng tôi đã thống nhất:

## Ưu tiên: Mật mã(học!) mới

Nhiều primitives (nguyên thủy) và giao thức hiện nay vẫn giữ nguyên các thiết kế ban đầu từ khoảng năm 2005 và cần được cải thiện. Chúng tôi đã có một số đề xuất mở trong vài năm với các ý tưởng, nhưng tiến triển đã chậm. Tất cả chúng tôi đều đồng ý rằng đây cần phải là ưu tiên hàng đầu của chúng tôi cho năm 2018. Các thành phần cốt lõi là:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

Công việc liên quan đến ưu tiên này được chia thành một số lĩnh vực:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Chúng tôi không thể phát hành các đặc tả giao thức mới trên toàn bộ mạng nếu chưa thực hiện công việc trên tất cả các lĩnh vực này.

## Nice-to-have: Code reuse

Một trong những lợi ích của việc bắt đầu công việc nêu trên ngay bây giờ là trong vài năm qua đã có những nỗ lực độc lập nhằm tạo ra các giao thức đơn giản và các khung giao thức đáp ứng được nhiều mục tiêu chúng tôi đặt ra cho các giao thức của chính mình, và đã được cộng đồng rộng rãi đón nhận. Bằng cách tận dụng những thành quả này, chúng tôi đạt được tác dụng "force multiplier" (khuếch đại tác động):

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Đặc biệt, các đề xuất của tôi sẽ tận dụng [Noise Protocol Framework](https://noiseprotocol.org/), và [định dạng gói SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Tôi đã sắp xếp hợp tác với một số người ngoài I2P cho các đề xuất này!

## Ưu tiên: Hợp tác trên Clearnet (mạng Internet công khai)

Liên quan đến chủ đề đó, trong khoảng sáu tháng qua chúng tôi đã dần dần khơi dậy được sự quan tâm. Tại PETS2017, 34C3 và RWC2018, tôi đã có những cuộc thảo luận rất tốt về cách chúng ta có thể cải thiện việc hợp tác với cộng đồng rộng lớn hơn. Điều này thực sự quan trọng để bảo đảm chúng ta có thể nhận được nhiều đánh giá nhất có thể cho các giao thức mới. Rào cản lớn nhất mà tôi thấy là phần lớn sự hợp tác phát triển I2P hiện đang diễn ra bên trong chính I2P, điều này làm tăng đáng kể công sức cần thiết để đóng góp.

Hai ưu tiên trong lĩnh vực này là:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Các mục tiêu khác được xếp vào loại nên có:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Tôi kỳ vọng rằng các hoạt động hợp tác với những người bên ngoài I2P sẽ được thực hiện hoàn toàn trên GitHub, để giảm thiểu trở ngại.

## Ưu tiên: Chuẩn bị cho các bản phát hành dài hạn

I2P hiện đã có trong Debian Sid (kho "unstable" của họ), vốn sẽ ổn định trong khoảng một năm rưỡi, và cũng đã được đưa vào kho lưu trữ của Ubuntu để đưa vào bản phát hành LTS tiếp theo vào tháng Tư. Chúng tôi sẽ bắt đầu có các phiên bản I2P lưu hành trong nhiều năm, và chúng tôi cần đảm bảo có thể xử lý sự hiện diện của chúng trong mạng.

Mục tiêu chính ở đây là triển khai càng nhiều giao thức mới nhất có thể trong năm tới, để kịp bản phát hành ổn định tiếp theo của Debian. Đối với những trường hợp cần lộ trình triển khai kéo dài nhiều năm, chúng ta nên đưa các thay đổi nhằm tương thích về sau (forward-compatability) vào càng sớm càng tốt.

## Ưu tiên: Plugin hóa các ứng dụng hiện có

Mô hình Debian khuyến khích tách thành các gói riêng cho từng thành phần. Chúng tôi đồng ý rằng việc tách rời các ứng dụng Java hiện đang được đóng gói kèm khỏi router Java cốt lõi sẽ mang lại lợi ích vì một số lý do:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Kết hợp với các ưu tiên trước đó, điều này đưa dự án I2P chính dịch chuyển nhiều hơn theo hướng giống như nhân Linux. Chúng tôi sẽ dành nhiều thời gian hơn tập trung vào chính mạng, còn nhường cho các nhà phát triển bên thứ ba tập trung vào các ứng dụng sử dụng mạng (việc này trở nên dễ dàng hơn đáng kể sau những công việc chúng tôi đã thực hiện trong vài năm qua đối với các API và thư viện).

## Nên có: Cải tiến ứng dụng

Có một loạt cải tiến ở cấp ứng dụng mà chúng tôi muốn thực hiện, nhưng hiện chúng tôi không có đủ thời gian của nhà phát triển để làm điều đó, do các ưu tiên khác. Đây là một lĩnh vực mà chúng tôi rất mong có thêm cộng tác viên mới! Sau khi việc tách rời nêu trên hoàn tất, sẽ dễ dàng hơn đáng kể để ai đó làm việc trên một ứng dụng cụ thể một cách độc lập với router Java chính.

Một trong những ứng dụng mà chúng tôi rất mong được hỗ trợ là I2P Android. Chúng tôi sẽ giữ ứng dụng này luôn được cập nhật theo các bản phát hành I2P cốt lõi và sửa lỗi khi có thể, nhưng vẫn còn rất nhiều điều có thể làm để cải thiện cả mã nền lẫn tính dễ sử dụng.

## Ưu tiên: ổn định Susimail và I2P-Bote

Mặc dù vậy, trong ngắn hạn chúng tôi thực sự muốn tập trung xử lý các bản sửa lỗi cho Susimail và I2P-Bote (một số đã được tích hợp vào 0.9.33). Trong vài năm qua, chúng ít được đầu tư phát triển hơn so với các ứng dụng I2P khác, vì vậy chúng tôi muốn dành thời gian đưa cơ sở mã nguồn của chúng lên ngang tầm và giúp chúng dễ tiếp cận hơn để người đóng góp mới có thể tham gia!

## Nên có: Ticket triage (phân loại/ưu tiên ticket)

Chúng tôi có một lượng lớn ticket tồn đọng trong một số phân hệ và ứng dụng của I2P. Là một phần của nỗ lực ổn định hóa nêu trên, chúng tôi rất muốn dọn dẹp một số vấn đề tồn đọng lâu năm của mình. Quan trọng hơn, chúng tôi muốn bảo đảm các ticket của mình được sắp xếp đúng cách, để những người đóng góp mới có thể tìm được các ticket phù hợp để làm việc.

## Ưu tiên: Hỗ trợ người dùng

Một khía cạnh của những điều nêu trên mà chúng tôi sẽ tập trung là giữ liên lạc với những người dùng dành thời gian báo cáo sự cố. Xin cảm ơn! Vòng phản hồi càng ngắn thì chúng tôi càng có thể nhanh chóng giải quyết các vấn đề mà người dùng mới gặp phải, và khả năng họ tiếp tục tham gia vào cộng đồng càng cao.

## Chúng tôi rất mong nhận được sự giúp đỡ của bạn!


Tất cả những điều đó trông rất tham vọng, và đúng là như vậy! Nhưng nhiều hạng mục ở trên chồng chéo nhau, và với việc lập kế hoạch cẩn thận, chúng ta có thể tạo ra bước tiến đáng kể đối với chúng.

Nếu bạn quan tâm hỗ trợ bất kỳ mục tiêu nào ở trên, hãy đến trò chuyện với chúng tôi! Bạn có thể tìm thấy chúng tôi trên OFTC và Freenode (#i2p-dev), cũng như Twitter (@GetI2P).
