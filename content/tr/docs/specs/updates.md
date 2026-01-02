---
title: "Yazılım Güncelleme Spesifikasyonu"
description: "I2P routers için güvenli, imzalı güncelleme mekanizması ve besleme yapısı"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

Router'lar, I2P ağı aracılığıyla dağıtılan imzalı bir haber akışını periyodik olarak sorgulayarak güncellemeleri otomatik olarak denetler. Daha yeni bir sürüm duyurulduğunda, router kriptografik olarak imzalanmış bir güncelleme arşivini (`.su3`) indirir ve kuruluma hazırlar. Bu sistem, resmi sürümlerin **kimliği doğrulanmış, kurcalamaya karşı dayanıklı** ve **çok kanallı** dağıtımını sağlar.

I2P 2.10.0 itibarıyla, güncelleme sistemi şunları kullanır:
- **RSA-4096 / SHA-512** imzaları
- **SU3 kapsayıcı biçimi** (eski SUD/SU2'nin yerini alır)
- **Yedekli yansılar:** ağ içi HTTP, clearnet (açık internet) HTTPS ve BitTorrent

---

## 1. Haber Kaynağı

Routers, yeni sürümleri ve güvenlik duyurularını keşfetmek için imzalı Atom akışını her birkaç saatte bir sorgular.   Akış imzalanır ve `.su3` dosyası olarak dağıtılır; şu öğeleri içerebilir:

- `<i2p:version>` — yeni sürüm numarası  
- `<i2p:minVersion>` — desteklenen en düşük router sürümü  
- `<i2p:minJavaVersion>` — gerekli en düşük Java çalışma zamanı  
- `<i2p:update>` — birden çok indirme aynasını listeler (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — sertifika iptal verileri  
- `<i2p:blocklist>` — ele geçirilmiş eşler için ağ düzeyi engelleme listeleri

### Besleme Dağıtımı

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Router'lar I2P beslemesini tercih eder, ancak gerekirse clearnet veya torrent dağıtımına geri dönebilir.

---

## 2. Dosya Biçimleri

### SU3 (Güncel Standart)

0.9.9 sürümünde tanıtılan SU3, eski SUD ve SU2 formatlarının yerini aldı.   Her dosya bir başlık, payload (yük) ve sonda yer alan bir imza içerir.

**Başlık Yapısı** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**İmza Doğrulama Adımları** 1. Başlığı ayrıştırın ve imza algoritmasını belirleyin.   2. İmzalayanın saklanan sertifikasını kullanarak özeti ve imzayı doğrulayın.   3. İmzalayanın sertifikasının iptal edilmediğini doğrulayın.   4. Gömülü sürüm dizesini yük üstverisiyle karşılaştırın.

Routers, güvenilir imzalayıcı sertifikalarıyla (şu anda **zzz** ve **str4d**) birlikte gelir ve imzasız veya iptal edilmiş kaynakları reddeder.

### SU2 (Kullanımdan kaldırıldı)

- Pack200 (Java JAR arşivleri için bir sıkıştırma biçimi) ile sıkıştırılmış JAR'larda `.su2` uzantısı kullanıldı.  
- Java 14'te Pack200 (JEP 367) kullanımdan kaldırıldıktan sonra çıkarıldı.  
- I2P 0.9.48+ sürümünde devre dışı bırakıldı; artık tamamen ZIP sıkıştırması ile değiştirildi.

### SUD (Eski)

- Erken DSA-SHA1 ile imzalanmış ZIP formatı (0.9.9 öncesi).  
- İmzalayan kimliği veya başlık yok, bütünlük sınırlı.  
- Zayıf kriptografi ve sürüm zorlamasının olmaması nedeniyle yerini yenisine bıraktı.

---

## 3. Güncelleme İş Akışı

### 3.1 Başlık Doğrulaması

Router'lar, tam dosyaları indirmeden önce sürüm dizesini doğrulamak için yalnızca **SU3 header**'ı alır.   Bu, eski yansılarda ya da güncel olmayan sürümlerde bant genişliğinin boşa harcanmasını önler.

### 3.2 Tam İndirme

Üstbilgiyi doğruladıktan sonra, router tam `.su3` dosyasını şuralardan indirir: - Ağ içi eepsite yansıları (tercih edilir)   - HTTPS clearnet (açık internet) yansıları (yedek)   - BitTorrent (isteğe bağlı eş destekli dağıtım)

İndirmeler, tekrar deneme, zaman aşımı yönetimi ve yedek aynaya geçiş özellikleriyle standart I2PTunnel HTTP istemcilerini kullanır.

### 3.3 İmza Doğrulama

İndirilen her dosya şu aşamalardan geçer: - **İmza kontrolü:** RSA-4096/SHA512 doğrulaması   - **Sürüm eşleşmesi:** Başlık ile payload (yük) sürüm kontrolü   - **Eski sürüme düşürmeyi önleme:** Güncellemenin yüklü sürümden daha yeni olmasını sağlar

Geçersiz veya eşleşmeyen dosyalar hemen atılır.

### 3.4 Aşamalı Kurulum

Doğrulandıktan sonra: 1. ZIP içeriğini geçici dizine çıkarın   2. `deletelist.txt` içinde listelenen dosyaları silin   3. `lib/jbigi.jar` dahilse yerel kütüphaneleri değiştirin   4. İmzalayanın sertifikalarını `~/.i2p/certificates/` konumuna kopyalayın   5. Bir sonraki yeniden başlatmada uygulanmak üzere güncellemeyi `i2pupdate.zip`'e taşıyın

Güncelleme, bir sonraki başlatmada veya “Install update now” elle tetiklendiğinde otomatik olarak yüklenir.

---

## 4. Dosya Yönetimi

### deletelist.txt

Yeni içerikleri açmadan önce kaldırılacak kullanımdan kalkmış dosyaların düz metin listesi.

**Kurallar:** - Her satırda bir yol (yalnızca göreli yollar) - `#` ile başlayan satırlar yok sayılır - `..` ve mutlak yollar reddedilir

### Yerel kütüphaneler

Güncel olmayan veya uyumsuz yerel ikili dosyaları önlemek için: - `lib/jbigi.jar` varsa, eski `.so` veya `.dll` dosyaları silinir   - Platforma özgü kütüphanelerin yeniden çıkarılmasını sağlar

---

## 5. Sertifika Yönetimi

Routers güncellemeler veya haber akışındaki iptaller aracılığıyla **yeni imzalayıcı sertifikaları** alabilir.

- Yeni `.crt` dosyaları sertifika dizinine kopyalanır.  
- İptal edilmiş sertifikalar gelecekteki doğrulamalardan önce silinir.  
- Manuel kullanıcı müdahalesi gerektirmeden anahtar döndürmeyi destekler.

Tüm güncellemeler, **air-gapped signing systems** (ağdan yalıtılmış imzalama sistemleri) kullanılarak çevrimdışı olarak imzalanır.   Özel anahtarlar hiçbir zaman derleme sunucularında saklanmaz.

---

## 6. Geliştirici Yönergeleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Gelecek sürümler, post-kuantum imza entegrasyonunu (bkz. Proposal 169) ve yeniden üretilebilir derlemeleri inceleyecek.

---

## 7. Güvenliğe Genel Bakış

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Sürümleme

- Router: **2.10.0 (API 0.9.67)**  
- Anlamsal sürümleme `Major.Minor.Patch` ile.  
- Minimum sürüm zorlaması güvensiz yükseltmeleri önler.
- Desteklenen Java: **Java 8–17**. Gelecek 2.11.0+ sürümleri Java 17+ gerektirecek.

---
