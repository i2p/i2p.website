---
title: "Thảo luận về đặt tên"
description: "Những tranh luận trong lịch sử về mô hình đặt tên của I2P và vì sao các phương án kiểu DNS toàn cục đã bị bác bỏ"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Bối cảnh:** Trang này lưu trữ lại các cuộc tranh luận kéo dài từ giai đoạn thiết kế I2P thời kỳ đầu. Nó giải thích vì sao dự án ưu tiên sổ địa chỉ tin cậy cục bộ thay vì tra cứu theo kiểu DNS hoặc các hệ thống đăng ký dựa trên biểu quyết đa số. Để biết hướng dẫn sử dụng hiện tại, xem [tài liệu Naming](/docs/overview/naming/).

## Các phương án thay thế đã bị loại bỏ

Các mục tiêu bảo mật của I2P loại trừ việc sử dụng các cơ chế đặt tên quen thuộc:

- **Phân giải kiểu DNS.** Bất kỳ trình phân giải nào trên tuyến tra cứu đều có thể giả mạo hoặc kiểm duyệt câu trả lời. Ngay cả với DNSSEC, các nhà đăng ký (registrar) hoặc tổ chức cấp chứng chỉ (CA) bị xâm phạm vẫn là một điểm lỗi đơn. Trong I2P, đích đến là khóa công khai—chiếm quyền một lần tra cứu sẽ làm lộ hoàn toàn một danh tính.
- **Đặt tên dựa trên bỏ phiếu.** Đối thủ có thể tạo ra vô hạn danh tính (Sybil attack: kẻ tấn công tạo nhiều danh tính giả) và “giành” phiếu cho các tên phổ biến. Các biện pháp giảm thiểu dựa trên proof-of-work (bằng chứng công việc) làm tăng chi phí nhưng kéo theo chi phí phối hợp lớn.

Thay vào đó, I2P cố ý giữ việc đặt tên ở phía trên tầng vận chuyển. Thư viện đặt tên đi kèm cung cấp một service-provider interface (giao diện nhà cung cấp dịch vụ) để các cơ chế thay thế có thể cùng tồn tại—người dùng quyết định những sổ địa chỉ hoặc jump services (dịch vụ “nhảy” để phân giải tên) mà họ tin cậy.

## Tên cục bộ và tên toàn cục (jrandom, 2005)

- Các tên trong I2P là **duy nhất cục bộ nhưng dễ đọc đối với con người**. `boss.i2p` của bạn có thể không khớp với `boss.i2p` của người khác, và điều đó là chủ ý.
- Nếu một tác nhân độc hại lừa bạn thay đổi destination (điểm đích) đằng sau một tên, họ sẽ chiếm đoạt một dịch vụ. Việc không đòi hỏi tính duy nhất toàn cục giúp ngăn chặn kiểu tấn công đó.
- Hãy coi các tên như dấu trang hoặc biệt danh IM—you choose which destinations to trust by subscribing to specific address books or adding keys manually.

## Các phản đối thường gặp & phản hồi (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Các ý tưởng về hiệu suất đã được thảo luận

- Cung cấp các bản cập nhật tăng dần (chỉ các đích (Destination) được thêm kể từ lần tải gần nhất).
- Cung cấp các nguồn cấp dữ liệu bổ sung (`recenthosts.cgi`) bên cạnh các tệp hosts đầy đủ.
- Khám phá các công cụ hỗ trợ script (ví dụ, `i2host.i2p`) để hợp nhất các nguồn cấp hoặc lọc theo mức độ tin cậy.

## Các điểm chính

- Bảo mật được ưu tiên hơn đồng thuận toàn cầu: sổ địa chỉ được quản lý cục bộ giúp giảm thiểu rủi ro chiếm đoạt.
- Nhiều cách tiếp cận đặt tên có thể cùng tồn tại thông qua naming API (API đặt tên)—người dùng tự quyết định nên tin vào điều gì.
- Hệ thống đặt tên toàn cầu hoàn toàn phi tập trung vẫn là một vấn đề nghiên cứu còn bỏ ngỏ; những đánh đổi giữa bảo mật, khả năng dễ ghi nhớ đối với con người và tính duy nhất toàn cầu vẫn phản ánh [tam giác của Zooko](https://zooko.com/distnames.html).

## Tài liệu tham khảo

- [Tài liệu về đặt tên](/docs/overview/naming/)
- [“Tên: Phi tập trung, Bảo mật, Có ý nghĩa với con người: Chọn hai” của Zooko](https://zooko.com/distnames.html)
- Mẫu nguồn cấp dữ liệu tăng dần: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
