---
title: "Garlic Yönlendirme"
description: "I2P'de garlic routing terminolojisini, mimarisini ve modern uygulamasını anlamak"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Genel Bakış

**Garlic routing**, I2P'nin temel yeniliklerinden biri olmaya devam etmektedir ve katmanlı şifreleme, mesaj paketleme ve tek yönlü tünelleri bir araya getirir. Kavramsal olarak **onion routing** ile benzer olsa da, birden fazla şifrelenmiş mesajı ("cloves") tek bir zarf içinde ("garlic") paketleyerek modeli genişletir ve böylece verimliliği ve anonimliği artırır.

*Garlic routing* terimi, [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) tarafından [Roger Dingledine'ın Free Haven Yüksek Lisans Tezi](https://www.freehaven.net/papers.html)'nde (Haziran 2000, §8.1.1) ortaya atılmıştır. I2P geliştiricileri, 2000'li yılların başında bu terimi, Tor'un devre anahtarlamalı tasarımından farklı olarak, paket gruplama iyileştirmelerini ve tek yönlü taşıma modelini yansıtmak için benimsemişlerdir.

> **Özet:** Garlic routing = katmanlı şifreleme + mesaj paketleme + tek yönlü tüneller üzerinden anonim teslimat.

---

## 2. "Garlic" Terminolojisi

Tarihsel olarak, *garlic* terimi I2P içinde üç farklı bağlamda kullanılmıştır:

1. **Katmanlı şifreleme** – tünel seviyesinde soğan tarzı koruma  
2. **Birden fazla mesajı paketleme** – bir "garlic message" içinde birden fazla "clove"  
3. **Uçtan uca şifreleme** – eskiden *ElGamal/AES+SessionTags*, şimdi *ECIES‑X25519‑AEAD‑Ratchet*

Mimari bozulmadan kalırken, şifreleme şeması tamamen modernize edilmiştir.

---

## 3. Katmanlı Şifreleme

Garlic routing, temel prensibini onion routing ile paylaşır: her router yalnızca bir şifreleme katmanını çözer, sadece bir sonraki atlamayı öğrenir ve tam yolu öğrenemez.

Ancak, I2P **tek yönlü tüneller** uygular, çift yönlü devreler değil:

- **Outbound tunnel**: mesajları oluşturucudan uzağa gönderir  
- **Inbound tunnel**: mesajları oluşturucuya geri taşır

Tam bir gidiş-dönüş (Alice ↔ Bob) dört tunnel kullanır: Alice'in outbound'u → Bob'un inbound'u, ardından Bob'un outbound'u → Alice'in inbound'u. Bu tasarım, çift yönlü devrelere kıyasla **korelasyon veri maruziyetini yarıya indirir**.

Tünel uygulama detayları için [Tünel Spesifikasyonu](/docs/specs/implementation) ve [Tünel Oluşturma (ECIES)](/docs/specs/implementation) spesifikasyonuna bakın.

---

## 4. Birden Fazla Mesajı Paketleme ("Cloves")

Freedman'ın orijinal garlic routing tasarımı, bir mesaj içinde birden fazla şifrelenmiş "bulb" (soğan dilimi) paketlemeyi öngörüyordu. I2P bunu bir **garlic message** içindeki **clove** (karanfil) olarak uygular — her clove'un kendi şifrelenmiş teslimat talimatları ve hedefi (router, destination veya tunnel) vardır.

Garlic bundling, I2P'nin şunları yapmasına olanak tanır:

- Onayları ve meta verileri veri mesajlarıyla birleştirin
- Gözlemlenebilir trafik desenlerini azaltın
- Ekstra bağlantı olmadan karmaşık mesaj yapılarını destekleyin

![Garlic Message Cloves](/images/garliccloves.png)   *Şekil 1: Her biri kendi teslimat talimatlarına sahip birden fazla dilim içeren bir Garlic Message.*

Tipik karanfiller şunları içerir:

1. **Teslimat Durumu Mesajı** — teslimat başarısını veya başarısızlığını onaylayan bildirimler.  
   Bunlar, gizliliği korumak için kendi garlic encryption katmanlarına sarılır.
2. **Veritabanı Depolama Mesajı** — eşlerin netDb'yi yeniden sorgulamadan yanıt verebilmesi için otomatik olarak paketlenen LeaseSet'ler.

Clove'lar aşağıdaki durumlarda paketlenir:

- Yeni bir LeaseSet yayınlanmalıdır
- Yeni oturum etiketleri teslim edilir
- Yakın zamanda herhangi bir paketleme gerçekleşmemiştir (~varsayılan olarak 1 dakika)

Garlic mesajları, tek bir pakette birden fazla şifrelenmiş bileşenin verimli uçtan uca iletimini sağlar.

---

## 5. Şifreleme Evrimi

### 5.1 Historical Context

Erken dönem dokümantasyon (≤ v0.9.12) *ElGamal/AES+SessionTags* şifrelemesini tanımlamıştır:   - **ElGamal 2048‑bit** ile sarmalanmış AES oturum anahtarları   - Yük şifrelemesi için **AES‑256/CBC**   - Mesaj başına bir kez kullanılan 32‑bayt oturum etiketleri

Bu kriptosistem **kullanımdan kaldırılmıştır**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

2019 ile 2023 yılları arasında, I2P tamamen ECIES‑X25519‑AEAD‑Ratchet'e geçiş yaptı. Modern yığın aşağıdaki bileşenleri standartlaştırır:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
ECIES geçişinin faydaları:

- **İleri gizlilik** mesaj başına değişen anahtarlar aracılığıyla  
- ElGamal'e kıyasla **daha küçük yük boyutu**  
- Kriptanalitik gelişmelere karşı **dayanıklılık**  
- Gelecekteki kuantum-sonrası hibrit sistemlerle **uyumluluk** (bkz. Öneri 169)

Ek detaylar: [ECIES Spesifikasyonu](/docs/specs/ecies) ve [EncryptedLeaseSet spesifikasyonu](/docs/specs/encryptedleaseset) belgelerine bakınız.

---

## 6. LeaseSets and Garlic Bundling

Garlic zarflar, hedef erişilebilirliğini yayınlamak veya güncellemek için sıklıkla LeaseSet'ler içerir.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Tüm LeaseSet'ler, özel yönlendiriciler tarafından yönetilen *floodfill DHT* üzerinden dağıtılır. Yayınlar doğrulanır, zaman damgası ile işaretlenir ve metadata korelasyonunu azaltmak için hız sınırlamasına tabi tutulur.

Detaylar için [Network Database belgelerine](/docs/specs/common-structures) bakın.

---

## 7. Modern “Garlic” Applications within I2P

Garlic encryption ve mesaj paketleme, I2P protokol yığınının tamamında kullanılır:

1. **Tunnel oluşturma ve kullanımı** — her atlama için katmanlı şifreleme  
2. **Uçtan uca mesaj iletimi** — klonlanmış-onay ve LeaseSet clove'ları ile paketlenmiş garlic mesajları  
3. **Network Database yayınlama** — gizlilik için garlic zarflarına sarılmış LeaseSet'ler  
4. **SSU2 ve NTCP2 aktarımları** — Noise çerçevesi ve X25519/ChaCha20 temel bileşenleri kullanılarak alt katman şifrelemesi

Garlic routing bu nedenle hem bir *şifreleme katmanlama yöntemi* hem de bir *ağ mesajlaşma modeli*dir.

---

## 6. LeaseSet'ler ve Garlic Paketleme

I2P'nin dokümantasyon merkezi [buradan ulaşılabilir](/docs/), sürekli güncellenir. İlgili güncel teknik özellikler şunlardır:

- [ECIES Spesifikasyonu](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel Oluşturma (ECIES)](/docs/specs/implementation) — modern tunnel inşa protokolü
- [I2NP Spesifikasyonu](/docs/specs/i2np) — I2NP mesaj formatları
- [SSU2 Spesifikasyonu](/docs/specs/ssu2) — SSU2 UDP taşıma protokolü
- [Ortak Yapılar](/docs/specs/common-structures) — netDb ve floodfill davranışı

Akademik doğrulama: Hoang ve diğerleri (IMC 2018, USENIX FOCI 2019) ve Muntaka ve diğerleri (2025), I2P'nin tasarımının mimari istikrarını ve operasyonel dayanıklılığını doğrulamaktadır.

---

## 7. I2P İçindeki Modern "Garlic" Uygulamaları

Devam eden öneriler:

- **Öneri 169:** Hibrit kuantum-sonrası (ML-KEM 512/768/1024 + X25519)  
- **Öneri 168:** Taşıma bant genişliği optimizasyonu  
- **Datagram ve akış güncellemeleri:** Gelişmiş tıkanıklık yönetimi

Gelecekteki uyarlamalar, Freedman tarafından başlangıçta tanımlanan kullanılmayan teslimat seçenekleri üzerine inşa edilerek, garlic-message seviyesinde ek mesaj geciktirme stratejileri veya çoklu tünel yedekliliği içerebilir.

---

## 8. Mevcut Dokümantasyon ve Referanslar

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
