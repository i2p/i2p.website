---
title: "Datagramlar"
description: "I2CP üzerinde kimlik doğrulamalı, yanıtlanabilir ve ham mesaj formatları"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Genel Bakış

Datagramlar, [I2CP](/docs/specs/i2cp/) üzerinde ve streaming kütüphanesine paralel olarak mesaj odaklı iletişim sağlar. Bağlantı odaklı stream'ler gerektirmeden **yanıtlanabilir**, **doğrulanmış** veya **ham** paketleri mümkün kılarlar. Router'lar, trafiği NTCP2 veya SSU2'nin taşımasına bakılmaksızın, datagramları I2NP mesajlarına ve tunnel mesajlarına kapsüller.

Temel motivasyon, uygulamaların (tracker'lar, DNS çözümleyiciler veya oyunlar gibi) gönderenlerini tanımlayan bağımsız paketler göndermelerine izin vermektir.

> **2025'te Yeni:** I2P Projesi, on yıl içinde ilk kez tekrar oynatma koruması ve daha düşük yük gerektiren yanıtlanabilir mesajlaşma ekleyen **Datagram2 (protokol 19)** ve **Datagram3 (protokol 20)**'yi onayladı.

---

## 1. Protokol Sabitleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Protokol 19 ve 20, **Öneri 163 (Nisan 2025)** ile resmileştirildi. Geriye dönük uyumluluk için Datagram1 / RAW ile birlikte bulunurlar.

---

## 2. Datagram Türleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Tipik Tasarım Kalıpları

- **İstek → Yanıt:** İmzalı bir Datagram2 gönderin (istek + nonce), ham veya Datagram3 yanıtı alın (nonce'u yankılayın).  
- **Yüksek frekanslı/düşük yük:** Datagram3 veya RAW tercih edin.  
- **Kimlik doğrulamalı kontrol mesajları:** Datagram2.  
- **Eski sürüm uyumluluğu:** Datagram1 hala tam olarak desteklenmektedir.

---

## 3. Datagram2 ve Datagram3 Detayları (2025)

### Datagram2 (Protokol 19)

Datagram1 için geliştirilmiş yedek. Özellikler: - **Tekrar saldırısı önleme:** 4 baytlık tekrar önleme belirteci. - **Çevrimdışı imza desteği:** çevrimdışı imzalı Destination'lar tarafından kullanımı mümkün kılar. - **Genişletilmiş imza kapsamı:** destination hash'i, bayrakları, seçenekleri, çevrimdışı imza bloğunu ve yükü içerir. - **Kuantum sonrası hazır:** gelecekteki ML-KEM hibrit çözümleriyle uyumlu. - **Ek yük:** ≈ 457 bayt (X25519 anahtarları).

### Datagram3 (Protokol 20)

Ham ve imzalı tipler arasındaki boşluğu kapatır. Özellikler: - **İmzasız yanıtlanabilir:** gönderenin 32-byte hash'ini + 2-byte bayrakları içerir. - **Küçük ek yük:** ≈ 34 byte. - **Tekrar saldırısı koruması yok** — uygulama tarafından uygulanmalıdır.

Her iki protokol de API 0.9.66 özellikleridir ve Sürüm 2.9.0'dan beri Java router'ında uygulanmıştır; henüz i2pd veya Go uygulamaları yoktur (Ekim 2025).

---

## 4. Boyut ve Parçalama Sınırları

- **Tunnel mesaj boyutu:** 1 028 bayt (4 B Tunnel ID + 16 B IV + 1 008 B yük verisi).  
- **İlk parça:** 956 B (tipik TUNNEL teslimi).  
- **Takip eden parça:** 996 B.  
- **Maksimum parça sayısı:** 63–64.  
- **Pratik sınır:** ≈ 62 708 B (~61 KB).  
- **Önerilen sınır:** Güvenilir teslimat için ≤ 10 KB (bu değerin ötesinde kayıplar üstel olarak artar).

**Ek yük özeti:** - Datagram1 ≈ 427 B (minimum).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Ek katmanlar (I2CP gzip başlığı, I2NP, Garlic, Tunnel): + ~5,5 KB en kötü durumda.

---

## 5. I2CP / I2NP Entegrasyonu

Mesaj yolu: 1. Uygulama datagram oluşturur (I2P API veya SAM aracılığıyla).   2. I2CP, gzip başlığı (`0x1F 0x8B 0x08`, RFC 1952) ve CRC-32 sağlama toplamı ile sarar.   3. Protokol + Port numaraları gzip başlık alanlarında saklanır.   4. Router, I2NP mesajı → Garlic clove → 1 KB tunnel parçaları olarak kapsüller.   5. Parçalar outbound → ağ → inbound tunnel üzerinden geçer.   6. Yeniden birleştirilen datagram, protokol numarasına göre uygulama işleyicisine teslim edilir.

**Bütünlük:** CRC-32 (I2CP'den) + isteğe bağlı kriptografik imza (Datagram1/2). Datagram'ın kendisi içinde ayrı bir sağlama toplamı alanı yoktur.

---

## 6. Programlama Arayüzleri

### Java API

`net.i2p.client.datagram` paketi şunları içerir: - `I2PDatagramMaker` – imzalı datagramlar oluşturur.   - `I2PDatagramDissector` – gönderen bilgisini doğrular ve çıkarır.   - `I2PInvalidDatagramException` – doğrulama başarısız olduğunda fırlatılır.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`), bir Destination'ı paylaşan uygulamalar için protokol ve port çoklama (multiplexing) işlemini yönetir.

**Javadoc erişimi:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (yalnızca I2P ağı) - [Javadoc Yansı](https://eyedeekay.github.io/javadoc-i2p/) (clearnet yansısı) - [Resmi Javadocs](http://docs.i2p-projekt.de/javadoc/) (resmi belgeler)

### SAM v3 Desteği

- SAM 3.2 (2016): PORT ve PROTOCOL parametreleri eklendi.  
- SAM 3.3 (2016): PRIMARY/alt oturum modeli tanıtıldı; bir Destination üzerinde akışlar + datagramlara izin verir.  
- Datagram2 / 3 oturum stilleri için destek 2025 spesifikasyonuna eklendi (uygulama beklemede).  
- Resmi spesifikasyon: [SAM v3 Specification](/docs/api/samv3/)

### i2ptunnel Modülleri

- **udpTunnel:** I2P UDP uygulamaları için tamamen işlevsel temel (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** A/V akışı için çalışır durumda (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** 2.10.0 sürümü itibariyle **işlevsel değil** (yalnızca UDP taslağı).

> Genel amaçlı UDP için Datagram API veya udpTunnel'ı doğrudan kullanın—SOCKS UDP'ye güvenmeyin.

---

## 7. Ekosistem ve Dil Desteği (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P şu anda tam SAM 3.3 alt oturumlarını ve Datagram2 API'sini destekleyen tek router'dır.

---

## 8. Örnek Kullanım – UDP Tracker (I2PSnark 2.10.0)

Datagram2/3'ün ilk gerçek dünya uygulaması:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Desen, güvenlik ve performansı dengelemek için doğrulanmış ve hafif datagramların karma kullanımını gösterir.

---

## 9. Güvenlik ve En İyi Uygulamalar

- Kimlik doğrulaması gerektiren veya tekrar saldırılarının önemli olduğu durumlarda Datagram2 kullanın.
- Orta düzeyde güven ile hızlı yanıtlanabilir cevaplar için Datagram3'ü tercih edin.
- Genel yayınlar veya anonim veri için RAW kullanın.
- Güvenilir teslimat için yükleri ≤ 10 KB tutun.
- SOCKS UDP'nin çalışmadığını unutmayın.
- Alındığında her zaman gzip CRC ve dijital imzaları doğrulayın.

---

## 10. Teknik Özellikler

Bu bölüm, düşük seviyeli datagram formatlarını, kapsüllemeyi ve protokol ayrıntılarını kapsar.

### 10.1 Protokol Tanımlama

Datagram formatları ortak bir başlık **paylaşmaz**. Router'lar sadece yük baytlarından türü çıkaramaz.

Birden fazla datagram türünü karıştırırken—veya datagramları akış ile birleştirirken—açıkça ayarlayın: - **Protokol numarasını** (I2CP veya SAM aracılığıyla) - Uygulamanız hizmetleri çoğulluyorsa isteğe bağlı olarak **port numarasını**

Protokolü ayarlanmamış bırakmak (`0` veya `PROTO_ANY`) önerilmez ve yönlendirme veya iletim hatalarına yol açabilir.

### 10.2 Ham Datagramlar

Yanıtlanamaz datagramlar gönderen veya kimlik doğrulama verisi taşımaz. Bunlar opak yüklerdir, üst düzey datagram API'sinin dışında işlenir ancak SAM ve I2PTunnel aracılığıyla desteklenir.

**Protokol:** `18` (`PROTO_DATAGRAM_RAW`)

**Biçim:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
Payload uzunluğu taşıma limitleriyle kısıtlanmıştır (pratik maksimum ≈32 KB, genellikle çok daha az).

### 10.3 Datagram1 (Yanıtlanabilir Datagramlar)

Gönderenin **Destination** bilgisini ve kimlik doğrulama ile yanıt adresleme için bir **Signature** içerir.

**Protokol:** `17` (`PROTO_DATAGRAM`)

**Ek Yük:** ≥427 bayt **Yük:** ~31,5 KB'a kadar (taşıma ile sınırlı)

**Format:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: bir Destination (387+ bayt)
- `signature`: anahtar tipiyle eşleşen bir İmza
  - DSA_SHA1 için: Yükün SHA-256 hash'inin İmzası
  - Diğer anahtar tipleri için: Doğrudan yük üzerindeki İmza

**Notlar:** - DSA olmayan türler için imzalar I2P 0.9.14'te standartlaştırılmıştır. - LS2 (Öneri 123) çevrimdışı imzalar şu anda Datagram1'de desteklenmemektedir.

### 10.4 Datagram2 Formatı

[Öneri 163](/proposals/163-datagram2/)'te tanımlandığı gibi **tekrar saldırısı direnci** ekleyen geliştirilmiş yanıtlanabilir datagram.

**Protokol:** `19` (`PROTO_DATAGRAM2`)

Uygulama devam etmektedir. Uygulamalar, yedeklilik için nonce veya zaman damgası kontrolleri içermelidir.

### 10.5 Datagram3 Formatı

**Yanıtlanabilir ancak doğrulanmamış** datagramlar sağlar. Gömülü hedef ve imza yerine router tarafından sağlanan oturum doğrulamasına dayanır.

**Protokol:** `20` (`PROTO_DATAGRAM3`) **Durum:** 0.9.66'dan beri geliştirme aşamasında

Yararlı olduğu durumlar: - Hedefler büyük olduğunda (örn., kuantum sonrası anahtarlar) - Kimlik doğrulama başka bir katmanda gerçekleştiğinde - Bant genişliği verimliliği kritik olduğunda

### 10.6 Veri Bütünlüğü

Datagram bütünlüğü, I2CP katmanındaki **gzip CRC-32 sağlama toplamı** tarafından korunur. Datagram yük biçiminin içinde açık bir sağlama toplamı alanı bulunmaz.

### 10.7 Paket Kapsülleme

Her datagram, tek bir I2NP mesajı veya bir **Garlic Message** içinde ayrı bir clove olarak kapsüllenir. I2CP, I2NP ve tunnel katmanları uzunluk ve çerçeveleme işlemlerini yönetir — datagram protokolünde dahili bir sınırlayıcı veya uzunluk alanı bulunmaz.

### 10.8 Kuantum Sonrası (PQ) Hususlar

Eğer **Proposal 169** (ML-DSA imzaları) uygulanırsa, imza ve hedef boyutları önemli ölçüde artacaktır — ~455 bayttan **≥3739 bayta** çıkacaktır. Bu değişiklik datagram ek yükünü önemli ölçüde artıracak ve etkili yük kapasitesini azaltacaktır.

**Datagram3**, oturum düzeyinde kimlik doğrulamaya dayanan (gömülü imzalar değil), kuantum-sonrası I2P ortamlarında muhtemelen tercih edilen tasarım haline gelecektir.

---

## 11. Referanslar

- [Öneri 163 – Datagram2 ve Datagram3](/proposals/163-datagram2/)
- [Öneri 160 – UDP Tracker Entegrasyonu](/proposals/160-udp-trackers/)
- [Öneri 144 – Streaming MTU Hesaplamaları](/proposals/144-ecies-x25519-aead-ratchet/)
- [Öneri 169 – Kuantum Sonrası İmzalar](/proposals/169-pq-crypto/)
- [I2CP Spesifikasyonu](/docs/specs/i2cp/)
- [I2NP Spesifikasyonu](/docs/specs/i2np/)
- [Tunnel Mesajı Spesifikasyonu](/docs/specs/implementation/)
- [SAM v3 Spesifikasyonu](/docs/api/samv3/)
- [i2ptunnel Dokümantasyonu](/docs/api/i2ptunnel/)

## 12. Değişiklik Günlüğü Öne Çıkanlar (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Özet

Datagram alt sistemi artık tamamen kimlik doğrulamalı iletimden hafif ham iletişime kadar bir yelpaze sunan dört protokol varyantını desteklemektedir. Geliştiriciler, güvenlik açısından hassas kullanım senaryoları için **Datagram2**'ye ve verimli yanıtlanabilir trafik için **Datagram3**'e geçiş yapmalıdır. Uzun vadeli birlikte çalışabilirliği sağlamak için tüm eski türler uyumlu kalmaya devam etmektedir.
