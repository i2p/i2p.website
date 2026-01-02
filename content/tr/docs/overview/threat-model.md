---
title: "I2P Tehdit Modeli"
description: "I2P'nin tasarımında değerlendirilen saldırı kataloğu ve mevcut önlemler"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. "Anonim" Ne Anlama Gelir

I2P *pratik anonimlik* sağlar—görünmezlik değil. Anonimlik, bir saldırganın gizli tutmak istediğiniz bilgileri öğrenmesinin zorluğu olarak tanımlanır: kim olduğunuz, nerede olduğunuz veya kiminle konuştuğunuz. Mutlak anonimlik imkansızdır; bunun yerine I2P, küresel pasif ve aktif saldırganlara karşı **yeterli anonimlik** hedefler.

Anonimliğiniz I2P'yi nasıl yapılandırdığınıza, eşleri ve abonelikleri nasıl seçtiğinize ve hangi uygulamaları açığa çıkardığınıza bağlıdır.

---

## 2. Kriptografik ve Taşıma Evrimi (2003 → 2025)

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
**Mevcut kriptografik paket (Noise XK):** - **X25519** anahtar değişimi için   - **ChaCha20/Poly1305 AEAD** şifreleme için   - **Ed25519 (EdDSA-SHA512)** imzalar için   - **SHA-256** hash işlemi ve HKDF için   - Kuantum sonrası testler için isteğe bağlı **ML-KEM hibrit** desteği

Tüm ElGamal ve AES-CBC kullanımları kullanımdan kaldırılmıştır. Taşıma tamamen NTCP2 (TCP) ve SSU2 (UDP) ile yapılır; her ikisi de IPv4/IPv6, ileri gizlilik (forward secrecy) ve DPI gizleme desteği sunar.

---

## 3. Ağ Mimarisi Özeti

- **Serbest rotali mixnet:** Gönderenler ve alıcılar kendi tunnel'larını kendileri tanımlar.  
- **Merkezi otorite yok:** Yönlendirme ve adlandırma merkeziyetsizdir; her router yerel güven bilgisini kendi tutar.  
- **Tek yönlü tunnel'lar:** Gelen ve giden ayrıdır (10 dakika ömür).  
- **Keşif tunnel'ları:** Varsayılan olarak 2 hop; istemci tunnel'ları 2–3 hop.  
- **Floodfill router'lar:** ~55 000 düğümün ~1 700'ü (~%6) dağıtık NetDB'yi korur.  
- **NetDB rotasyonu:** Anahtar uzayı her gün UTC gece yarısı döner.  
- **Alt-DB izolasyonu:** 2.4.0'dan beri her istemci ve router bağlantı kurmayı önlemek için ayrı veritabanları kullanır.

---

## 4. Saldırı Kategorileri ve Mevcut Savunmalar

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

## 5. Modern Network Database (NetDB)

**Temel gerçekler (hâlâ geçerli):** - Değiştirilmiş Kademlia DHT, RouterInfo ve LeaseSet'leri saklar.   - SHA-256 anahtar hash'leme; 10 s zaman aşımı ile en yakın 2 floodfill'e paralel sorgular.   - LeaseSet ömrü ≈ 10 dk (LeaseSet2) veya 18 s (MetaLeaseSet).

**Yeni türler (0.9.38'den beri):** - **LeaseSet2 (Tür 3)** – birden fazla şifreleme türü, zaman damgalı.   - **EncryptedLeaseSet2 (Tür 5)** – özel hizmetler için gizlenmiş hedef (DH veya PSK kimlik doğrulama).   - **MetaLeaseSet (Tür 7)** – çoklu barındırma ve genişletilmiş süre sonu.

**Önemli güvenlik yükseltmesi – Alt-DB İzolasyonu (2.4.0):** - Router↔istemci ilişkilendirmesini önler.   - Her istemci ve router ayrı netDb segmentleri kullanır.   - Doğrulandı ve denetlendi (2.5.0).

---

## 6. Gizli Mod ve Kısıtlanmış Rotalar

- **Gizli Mod (Hidden Mode):** Uygulandı (Freedom House puanlarına göre sıkı ülkelerde otomatik).  
    Router'lar RouterInfo yayınlamaz veya trafik yönlendirmez.  
- **Kısıtlı Rotalar (Restricted Routes):** Kısmen uygulandı (yalnızca temel güven tabanlı tunnel'lar).  
    Kapsamlı güvenilir-eş yönlendirmesi planlanıyor (3.0+).

Denge: Daha iyi gizlilik ↔ ağ kapasitesine katkının azalması.

---

## 7. DoS ve Floodfill Saldırıları

**Tarihsel:** 2013 UCSB araştırması Eclipse ve Floodfill ele geçirmelerinin mümkün olduğunu gösterdi. **Modern savunmalar şunları içerir:** - Günlük keyspace rotasyonu. - Floodfill sınırı ≈ 500, /16 başına bir. - Rastgele depolama doğrulama gecikmeleri. - Daha yeni router tercihi (2.6.0). - Otomatik kayıt düzeltmesi (2.9.0). - Tıkanıklık farkında yönlendirme ve lease kısıtlama (2.4.0+).

Floodfill saldırıları teorik olarak hala mümkün ancak pratikte daha zor.

---

## 8. Trafik Analizi ve Sansür

I2P trafiğini tespit etmek zordur: sabit port yok, düz metin el sıkışması yok ve rastgele dolgu kullanılır. NTCP2 ve SSU2 paketleri yaygın protokolleri taklit eder ve ChaCha20 başlık gizleme kullanır. Dolgu stratejileri temeldir (rastgele boyutlar), sahte trafik uygulanmamıştır (maliyetlidir). Tor çıkış düğümlerinden gelen bağlantılar 2.6.0 sürümünden beri engellenmiştir (kaynakları korumak için).

---

## 9. Kalıcı Kısıtlamalar (kabul edilmiş)

- Düşük gecikmeli uygulamalar için zamanlama korelasyonu temel bir risk olmaya devam ediyor.
- Bilinen genel hedeflere karşı kesişim saldırıları hala güçlü.
- Sybil saldırılarına karşı tam koruma eksik (HashCash zorunlu kılınmıyor).
- Sabit hızlı trafik ve önemsiz olmayan gecikmeler hala uygulanmadı (3.0'da planlandı).

Bu sınırlamalar hakkındaki şeffaflık kasıtlıdır — kullanıcıların anonimliği fazla tahmin etmesini önler.

---

## 10. Ağ İstatistikleri (2025)

- Dünya çapında ~55 000 aktif router (2013'teki 7 000'den ↑)  
- ~1 700 floodfill router (~%6)  
- Varsayılan olarak %95'i tunnel yönlendirmesine katılıyor  
- Bant genişliği katmanları: K (<12 KB/s) → X (>2 MB/s)  
- Minimum floodfill hızı: 128 KB/s  
- Router konsolu Java 8+ (gerekli), Java 17+ bir sonraki döngü için planlanıyor

---

## 11. Geliştirme ve Merkezi Kaynaklar

- Resmi site: [geti2p.net](/)
- Belgeler: [Documentation](/docs/)  
- Debian deposu: <https://deb.i2pgit.org> ( Ekim 2023'te deb.i2p2.de'nin yerini aldı )  
- Kaynak kodu: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub yansısı  
- Tüm sürümler imzalı SU3 konteynerlerdir (RSA-4096, zzz/str4d anahtarları)  
- Aktif e-posta listeleri yok; topluluk <https://i2pforum.net> ve IRC2P üzerinden.  
- Güncelleme döngüsü: 6–8 haftalık kararlı sürümler.

---

## 12. 0.8.x'ten Bu Yana Yapılan Güvenlik İyileştirmelerinin Özeti

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

## 13. Bilinen Çözülmemiş veya Planlanan Çalışmalar

- Kapsamlı kısıtlı yönlendirme (güvenilir eş yönlendirme) → 3.0 için planlanmış.  
- Zamanlama direnci için önemsiz olmayan gecikme/toplu işleme → 3.0 için planlanmış.  
- Gelişmiş dolgu ve sahte trafik → uygulanmamış.  
- HashCash kimlik doğrulama → altyapı mevcut ancak aktif değil.  
- R5N DHT değiştirmesi → sadece öneri.

---

## 14. Temel Referanslar

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [I2P Resmi Belgelendirmesi](/docs/)

---

## 15. Sonuç

I2P'nin temel anonimlik modeli yirmi yıldır ayakta: küresel benzersizliği yerel güven ve güvenlik için feda etmek. ElGamal'dan X25519'a, NTCP'den NTCP2'ye ve manuel yeniden tohumlamadan Sub-DB izolasyonuna kadar, proje derinlemesine savunma ve şeffaflık felsefesini koruyarak gelişti.

Düşük gecikmeli herhangi bir mixnet'e karşı birçok saldırı teorik olarak hala mümkün olsa da, I2P'nin sürekli güçlendirilmesi bu saldırıları giderek daha pratik olmayan hale getiriyor. Ağ her zamankinden daha büyük, daha hızlı ve daha güvenli — ancak yine de kendi sınırları konusunda dürüst.
