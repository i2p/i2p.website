---
title: "SSU (eski)"
description: "Özgün, güvenli ve yarı güvenilir UDP taşıması"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Kullanımdan kaldırıldı:** SSU'nun yerini SSU2 aldı. Desteği i2pd 2.44.0 (API 0.9.56, Kasım 2022) ve Java I2P 2.4.0 (API 0.9.61, Aralık 2023) sürümlerinden kaldırıldı.

SSU, tıkanıklık kontrolü, NAT geçişi ve introducer (tanıştırıcı) desteği ile UDP tabanlı, yarı güvenilir iletim sağladı. NAT/güvenlik duvarlarının arkasındaki router'ları ele alarak ve IP keşfini koordine ederek NTCP'yi tamamladı.

## Adres Öğeleri

- `transport`: `SSU`
- `caps`: yetenek bayrakları (`B`, `C`, `4`, `6`, vb.)
- `host` / `port`: IPv4 veya IPv6 dinleyici (güvenlik duvarı arkasındayken isteğe bağlı)
- `key`: Base64 tanıtma anahtarı
- `mtu`: İsteğe bağlı; varsayılan 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: router güvenlik duvarı arkasındayken introducer (tanıştırıcı) girdileri

## Özellikler

- introducers (tanıştırıcılar) kullanılarak işbirliğine dayalı NAT geçişi
- Eş testleri ve gelen paketlerin incelenmesi yoluyla yerel IP tespiti
- Güvenlik duvarı durumunun otomatik olarak diğer taşıma katmanlarına ve router konsoluna iletilmesi
- Yarı güvenilir teslimat: mesajlar bir sınıra kadar yeniden iletilir, ardından düşürülür
- Toplamsal artış / çarpımsal azalış ile tıkanıklık kontrolü ve parça ACK bit alanları

SSU ayrıca zamanlama işaretleri ve MTU müzakeresi gibi üstveri görevlerini de üstleniyordu. Artık tüm işlevler (modern kriptografi ile) [SSU2](/docs/specs/ssu2/) tarafından sağlanmaktadır.
