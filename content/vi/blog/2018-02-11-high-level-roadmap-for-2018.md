---
title: "Lộ trình tổng quan cho năm 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "Năm 2018 sẽ là năm của các giao thức mới, các hợp tác mới, và một trọng tâm được tinh chỉnh hơn."
categories: ["roadmap"]
---

Một trong nhiều điều chúng tôi đã thảo luận tại 34C3 là chúng tôi nên tập trung vào điều gì trong năm tới. Cụ thể, chúng tôi muốn có một lộ trình nêu rõ những việc chúng tôi muốn đảm bảo sẽ hoàn thành, so với những điều sẽ thật tuyệt nếu có, và đồng thời có thể giúp những người mới tham gia vào cả hai hạng mục đó. Dưới đây là những gì chúng tôi đã đưa ra:

## Ưu tiên: Mật mã học mới!

Nhiều primitives (các thành phần nguyên thủy) và giao thức hiện tại vẫn giữ nguyên thiết kế ban đầu từ khoảng năm 2005, và cần được cải thiện. Chúng tôi đã có một số đề xuất đang mở trong vài năm qua với các ý tưởng, nhưng tiến triển vẫn chậm. Tất cả chúng tôi đều đồng ý rằng đây cần phải là ưu tiên hàng đầu của chúng tôi cho năm 2018. Các thành phần cốt lõi là:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

Công việc cho ưu tiên này bao gồm một số lĩnh vực:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Chúng tôi không thể phát hành các đặc tả giao thức mới trên toàn bộ mạng nếu không làm việc trên tất cả các lĩnh vực này.

## Nên có: Tái sử dụng mã

Một trong những lợi ích của việc bắt đầu công việc nêu trên ngay bây giờ là trong vài năm gần đây đã có những nỗ lực độc lập nhằm tạo ra các giao thức và khung giao thức đơn giản đáp ứng nhiều mục tiêu mà chúng ta đặt ra cho các giao thức của riêng mình, và chúng đã được cộng đồng rộng rãi đón nhận. Bằng cách tận dụng những kết quả này, chúng ta đạt được hiệu ứng "force multiplier" (khuếch đại hiệu quả):

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Cụ thể, các đề xuất của tôi sẽ tận dụng [Noise Protocol Framework](https://noiseprotocol.org/), và [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Tôi đã thu xếp hợp tác với một số người bên ngoài I2P cho các đề xuất này!

## Ưu tiên: hợp tác với Clearnet

Về chủ đề đó, trong khoảng sáu tháng trở lại đây chúng tôi đã dần thu hút sự quan tâm. Tại PETS2017, 34C3 và RWC2018, tôi đã có một số cuộc thảo luận rất hữu ích về những cách thức chúng ta có thể cải thiện việc hợp tác với cộng đồng rộng lớn hơn. Điều này thực sự quan trọng để đảm bảo chúng ta có thể nhận được nhiều đánh giá nhất có thể cho các giao thức mới. Rào cản lớn nhất mà tôi thấy là thực tế phần lớn việc cộng tác phát triển I2P hiện đang diễn ra bên trong chính I2P, điều này làm tăng đáng kể công sức cần thiết để đóng góp.

Hai ưu tiên trong lĩnh vực này là:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Các mục tiêu khác được xếp vào loại nên có:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Tôi kỳ vọng rằng việc hợp tác với những người bên ngoài I2P sẽ được thực hiện hoàn toàn trên GitHub, nhằm giảm thiểu ma sát.

## Ưu tiên: Chuẩn bị cho các bản phát hành dài hạn

I2P hiện đã có trong Debian Sid (kho phần mềm "unstable" của họ), dự kiến sẽ ổn định trong khoảng một năm rưỡi, và cũng đã được đưa vào kho phần mềm của Ubuntu để được đưa vào bản phát hành LTS tiếp theo vào tháng 4. Chúng ta sẽ bắt đầu có các phiên bản I2P tồn tại trong nhiều năm, và chúng ta cần bảo đảm có thể xử lý sự hiện diện của chúng trong mạng.

Mục tiêu chính ở đây là triển khai càng nhiều giao thức mới càng tốt trong phạm vi khả thi trong năm tới, để kịp bản phát hành ổn định tiếp theo của Debian. Đối với những hạng mục cần nhiều năm để triển khai, chúng ta nên đưa các thay đổi nhằm đảm bảo tương thích về sau vào càng sớm càng tốt.

## Ưu tiên: Plugin hóa các ứng dụng hiện tại

Mô hình Debian khuyến khích có các gói riêng cho từng thành phần. Chúng tôi đồng ý rằng việc tách riêng các ứng dụng Java hiện đang được đóng gói kèm khỏi router Java cốt lõi sẽ có lợi vì một số lý do:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Kết hợp với các ưu tiên trước đó, điều này đưa dự án I2P chính tiến gần hơn theo hướng, ví dụ, nhân Linux. Chúng tôi sẽ dành nhiều thời gian hơn để tập trung vào chính mạng lưới, để các nhà phát triển bên thứ ba tập trung vào các ứng dụng sử dụng mạng lưới (điều này đã trở nên dễ dàng hơn đáng kể sau công việc chúng tôi đã thực hiện trong vài năm qua về API và thư viện).

## Nên có: Cải tiến ứng dụng

Có một loạt cải tiến ở cấp độ ứng dụng mà chúng tôi muốn thực hiện, nhưng hiện chưa có đủ thời gian của nhà phát triển để làm, do các ưu tiên khác của chúng tôi. Đây là một lĩnh vực mà chúng tôi rất mong có những người đóng góp mới! Khi việc tách rời (decoupling) nêu trên hoàn tất, sẽ dễ dàng hơn rất nhiều để ai đó làm việc trên một ứng dụng cụ thể một cách độc lập với Java router chính.

Một trong những ứng dụng như vậy mà chúng tôi rất mong nhận được sự hỗ trợ là I2P Android. Chúng tôi sẽ giữ cho nó luôn đồng bộ với các bản phát hành I2P cốt lõi và sửa lỗi khi có thể, nhưng vẫn còn nhiều việc có thể làm để cải thiện mã nền cũng như tính dễ sử dụng.

## Ưu tiên: ổn định Susimail và I2P-Bote

Mặc dù vậy, chúng tôi thực sự muốn tập trung vào các bản sửa lỗi cho Susimail và I2P-Bote trong thời gian ngắn sắp tới (một số trong đó đã được đưa vào 0.9.33). Trong vài năm qua, chúng nhận được ít cập nhật và cải tiến hơn so với các ứng dụng I2P khác, vì vậy chúng tôi muốn dành thời gian để đưa mã nguồn của chúng lên ngang tầm và giúp chúng dễ tiếp cận hơn để các cộng tác viên mới có thể nhanh chóng bắt tay vào!

## Nên có: Phân loại/ưu tiên ticket

Chúng tôi có một lượng lớn ticket (phiếu công việc) còn tồn đọng trong nhiều phân hệ và ứng dụng của I2P. Như một phần của nỗ lực ổn định hóa nêu trên, chúng tôi rất muốn dọn dẹp một số vấn đề cũ đã tồn tại lâu năm. Quan trọng hơn, chúng tôi muốn bảo đảm rằng các ticket được sắp xếp hợp lý, để những người đóng góp mới có thể tìm được các ticket phù hợp để làm.

## Ưu tiên: Hỗ trợ người dùng

Trong các nội dung nêu trên, một trọng tâm của chúng tôi là duy trì liên lạc với những người dùng dành thời gian báo cáo sự cố. Xin cảm ơn! Vòng phản hồi càng ngắn, chúng tôi càng có thể nhanh chóng giải quyết các vấn đề mà người dùng mới gặp phải, và khả năng họ tiếp tục tham gia vào cộng đồng càng cao.

## Chúng tôi rất mong nhận được sự giúp đỡ của bạn!


Nhìn chung tất cả có vẻ rất tham vọng, và đúng là như vậy! Nhưng nhiều hạng mục ở trên chồng chéo nhau, và với việc lập kế hoạch cẩn thận, chúng ta có thể giải quyết được một phần đáng kể trong số đó.

Nếu bạn quan tâm đến việc hỗ trợ bất kỳ mục tiêu nào ở trên, hãy tham gia trò chuyện với chúng tôi! Bạn có thể tìm chúng tôi trên OFTC và Freenode (#i2p-dev), cũng như trên Twitter (@GetI2P).
