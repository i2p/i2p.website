---
title: "Mô hình Mối đe dọa I2P"
description: "Danh mục các cuộc tấn công được xem xét trong thiết kế của I2P và các biện pháp giảm thiểu đã triển khai"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. "Ẩn danh" có nghĩa là gì

I2P cung cấp *tính ẩn danh thực tế*—không phải tàng hình. Tính ẩn danh được định nghĩa là mức độ khó khăn để đối thủ tìm hiểu thông tin bạn muốn giữ bí mật: bạn là ai, bạn ở đâu, hoặc bạn nói chuyện với ai. Tính ẩn danh tuyệt đối là không thể; thay vào đó, I2P hướng tới **tính ẩn danh đủ mức** trước các đối thủ thụ động và chủ động toàn cầu.

Tính ẩn danh của bạn phụ thuộc vào cách bạn cấu hình I2P, cách bạn chọn peer và subscription, và những ứng dụng nào bạn sử dụng.

---

## 2. Sự phát triển về Mật mã và Truyền tải (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**Bộ mã hóa hiện tại (Noise XK):** - **X25519** cho trao đổi khóa   - **ChaCha20/Poly1305 AEAD** cho mã hóa   - **Ed25519 (EdDSA-SHA512)** cho chữ ký   - **SHA-256** cho băm và HKDF   - Tùy chọn **ML-KEM hybrids** cho thử nghiệm hậu lượng tử

Tất cả các cách sử dụng ElGamal và AES-CBC đã bị loại bỏ. Truyền tải hoàn toàn sử dụng NTCP2 (TCP) và SSU2 (UDP); cả hai đều hỗ trợ IPv4/IPv6, forward secrecy (bảo mật chuyển tiếp), và obfuscation DPI (làm xáo trộn phát hiện gói tin sâu).

---

## 3. Tóm tắt Kiến trúc Mạng

- **Mixnet tự do định tuyến:** Người gửi và người nhận mỗi bên tự định nghĩa tunnel của riêng mình.  
- **Không có cơ quan trung tâm:** Định tuyến và đặt tên được phân tán; mỗi router duy trì lòng tin cục bộ.  
- **Tunnel một chiều:** Inbound và outbound được tách biệt (thời gian tồn tại 10 phút).  
- **Exploratory tunnels:** Mặc định 2 hops; client tunnels 2–3 hops.  
- **Floodfill routers:** ~1 700 trong số ~55 000 nodes (~6 %) duy trì NetDB phân tán.  
- **Luân chuyển NetDB:** Keyspace luân chuyển hàng ngày vào lúc nửa đêm UTC.  
- **Cô lập Sub-DB:** Từ phiên bản 2.4.0, mỗi client và router sử dụng các cơ sở dữ liệu riêng biệt để ngăn chặn việc liên kết.

---

## 4. Các loại tấn công và phương thức phòng thủ hiện tại

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. Cơ sở dữ liệu mạng hiện đại (NetDB)

**Các thông tin cốt lõi (vẫn chính xác):** - DHT Kademlia được sửa đổi để lưu trữ RouterInfo và LeaseSets.   - Băm khóa SHA-256; truy vấn song song đến 2 floodfills gần nhất với thời gian chờ 10 giây.   - Thời gian tồn tại của LeaseSet ≈ 10 phút (LeaseSet2) hoặc 18 giờ (MetaLeaseSet).

**Các loại mới (từ phiên bản 0.9.38):** - **LeaseSet2 (Loại 3)** – hỗ trợ nhiều kiểu mã hóa, có dấu thời gian.   - **EncryptedLeaseSet2 (Loại 5)** – destination được che dấu cho các dịch vụ riêng tư (xác thực DH hoặc PSK).   - **MetaLeaseSet (Loại 7)** – hỗ trợ nhiều địa chỉ và thời gian hết hạn mở rộng.

**Nâng cấp bảo mật quan trọng – Cô lập Sub-DB (2.4.0):** - Ngăn chặn liên kết router↔client.   - Mỗi client và router sử dụng các phân đoạn netDb riêng biệt.   - Đã được xác minh và kiểm toán (2.5.0).

---

## 6. Chế độ Ẩn và Định tuyến Hạn chế

- **Chế độ Ẩn (Hidden Mode):** Đã triển khai (tự động kích hoạt ở các quốc gia nghiêm ngặt theo điểm số Freedom House).  
    Router không công bố RouterInfo hoặc định tuyến lưu lượng.  
- **Định tuyến Hạn chế (Restricted Routes):** Đã triển khai một phần (chỉ tunnel tin cậy cơ bản).  
    Định tuyến ngang hàng tin cậy toàn diện vẫn đang được lên kế hoạch (3.0+).

Đánh đổi: Quyền riêng tư tốt hơn ↔ giảm đóng góp vào năng lực mạng.

---

## 7. Tấn công DoS và Floodfill

**Lịch sử:** Nghiên cứu năm 2013 của UCSB cho thấy khả năng xảy ra các cuộc tấn công Eclipse và chiếm quyền Floodfill.   **Các biện pháp phòng thủ hiện đại bao gồm:** - Xoay vòng keyspace hàng ngày.   - Giới hạn Floodfill ≈ 500, một router mỗi /16.   - Độ trễ xác minh lưu trữ ngẫu nhiên hóa.   - Ưu tiên router mới hơn (2.6.0).   - Sửa lỗi đăng ký tự động (2.9.0).   - Định tuyến nhận biết tắc nghẽn và điều tiết lease (2.4.0+).

Các cuộc tấn công floodfill vẫn có thể xảy ra về mặt lý thuyết nhưng khó thực hiện hơn trên thực tế.

---

## 8. Phân tích lưu lượng và kiểm duyệt

Lưu lượng I2P khó xác định: không có cổng cố định, không có bắt tay văn bản rõ, và có padding ngẫu nhiên. Các gói tin NTCP2 và SSU2 bắt chước các giao thức phổ biến và sử dụng kỹ thuật che giấu header ChaCha20. Các chiến lược padding còn cơ bản (kích thước ngẫu nhiên), lưu lượng giả không được triển khai (tốn kém). Các kết nối từ nút thoát Tor bị chặn kể từ phiên bản 2.6.0 (để bảo vệ tài nguyên).

---

## 9. Các hạn chế liên tục (đã được thừa nhận)

- Tương quan thời gian cho các ứng dụng độ trễ thấp vẫn là rủi ro cơ bản.
- Tấn công giao điểm vẫn mạnh mẽ chống lại các đích công khai đã biết.
- Tấn công Sybil thiếu phòng thủ hoàn chỉnh (HashCash chưa được thực thi).
- Lưu lượng tốc độ không đổi và độ trễ đáng kể vẫn chưa được triển khai (dự kiến 3.0).

Sự minh bạch về những giới hạn này là có chủ đích — nó ngăn người dùng đánh giá quá cao tính ẩn danh.

---

## 10. Thống kê Mạng (2025)

- ~55 000 router hoạt động trên toàn thế giới (↑ từ 7 000 vào năm 2013)  
- ~1 700 floodfill router (~6 %)  
- 95 % tham gia định tuyến tunnel theo mặc định  
- Các mức băng thông: K (<12 KB/s) → X (>2 MB/s)  
- Tốc độ floodfill tối thiểu: 128 KB/s  
- Bảng điều khiển Router yêu cầu Java 8+, dự kiến Java 17+ cho chu kỳ tiếp theo

---

## 11. Phát triển và Tài nguyên Trung tâm

- Trang chính thức: [geti2p.net](/)
- Tài liệu: [Documentation](/docs/)  
- Kho lưu trữ Debian: <https://deb.i2pgit.org> ( thay thế deb.i2p2.de vào tháng 10/2023 )  
- Mã nguồn: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + bản sao GitHub  
- Tất cả các bản phát hành đều là container SU3 có chữ ký (RSA-4096, khóa zzz/str4d)  
- Không có danh sách gửi thư hoạt động; cộng đồng qua <https://i2pforum.net> và IRC2P.  
- Chu kỳ cập nhật: phát hành bản ổn định mỗi 6–8 tuần.

---

## 12. Tóm tắt các Cải tiến Bảo mật từ phiên bản 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. Các Công Việc Chưa Giải Quyết hoặc Đã Lên Kế Hoạch

- Định tuyến hạn chế toàn diện (định tuyến ngang hàng tin cậy) → lên kế hoạch 3.0.
- Độ trễ/gộp lô đáng kể để chống phân tích thời gian → lên kế hoạch 3.0.
- Padding nâng cao và lưu lượng giả → chưa triển khai.
- Xác minh danh tính HashCash → cơ sở hạ tầng đã có nhưng chưa kích hoạt.
- Thay thế DHT bằng R5N → chỉ mới đề xuất.

---

## 14. Tài liệu Tham khảo Chính

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Tài liệu chính thức của I2P](/docs/)

---

## 15. Kết luận

Mô hình ẩn danh cốt lõi của I2P đã tồn tại được hai thập kỷ: hy sinh tính duy nhất toàn cầu để đổi lấy sự tin cậy và bảo mật cục bộ. Từ ElGamal đến X25519, NTCP đến NTCP2, và từ reseed thủ công đến cô lập Sub-DB, dự án đã phát triển trong khi vẫn duy trì triết lý phòng thủ theo chiều sâu và minh bạch.

Nhiều cuộc tấn công vẫn có thể xảy ra về mặt lý thuyết đối với bất kỳ mixnet độ trễ thấp nào, nhưng việc I2P liên tục tăng cường bảo mật khiến chúng ngày càng khó thực hiện hơn. Mạng lưới hiện lớn hơn, nhanh hơn và an toàn hơn bao giờ hết — nhưng vẫn trung thực về các giới hạn của nó.
