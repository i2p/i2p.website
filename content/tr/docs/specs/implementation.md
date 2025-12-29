---
title: "Tunnel İşlemleri Kılavuzu"
description: "I2P tunnel’larının kurulumu ile trafiğin şifrelenmesi ve iletilmesine yönelik birleşik bir belirtim."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Kapsam:** Bu kılavuz, tunnel uygulamasını, ileti biçimini ve her iki tunnel oluşturma belirtimini (ECIES (Eliptik Eğri Entegre Şifreleme Şeması) ve eski ElGamal (ElGamal şifreleme)) bir araya getirir. Mevcut derin bağlantılar yukarıdaki takma adlar aracılığıyla çalışmaya devam eder.

## Tunnel Modeli {#tunnel-model}

I2P, yükleri *tek yönlü tunnel'lar* üzerinden iletir: bunlar, trafiği tek bir yönde taşıyan sıralı router kümeleridir. İki hedef arasındaki tam bir gidiş-dönüş için dört tunnel gerekir (iki giden, iki gelen).

Terminoloji için [Tunnel Genel Bakışı](/docs/overview/tunnel-routing/) ile başlayın, ardından operasyonel ayrıntılar için bu kılavuzu kullanın.

### Mesaj Yaşam Döngüsü {#message-lifecycle}

1. tunnel **geçidi**, bir veya daha fazla I2NP mesajını toplar, bunları parçalara ayırır ve teslim talimatlarını yazar.
2. Geçit, yükü sabit boyutlu (1024&nbsp;B) bir tunnel mesajı içine kapsüller, gerekirse doldurma (padding) uygular.
3. Her **katılımcı**, önceki atlamayı (hop) doğrular, kendi şifreleme katmanını uygular ve `{nextTunnelId, nextIV, encryptedPayload}` değerini bir sonraki atlamaya iletir.
4. tunnel **uç noktası**, son katmanı kaldırır, teslim talimatlarını uygular, parçaları yeniden birleştirir ve yeniden oluşturulan I2NP mesajlarını iletir.

Yinelenenleri tespit etme, IV (başlangıç vektörü) ile ilk şifreli metin bloğunun XOR (dışlayan veya) işlemiyle elde edilen değeri anahtar olarak kullanan, zamana bağlı bozunan bir Bloom filtresi kullanır; bu, IV değiştirmeye dayalı etiketleme saldırılarını önler.

### Rollere Hızlı Bakış {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Şifreleme İş Akışı {#encryption-workflow}

- **Inbound tunnels:** ağ geçidi katman anahtarıyla bir kez şifreler; aşağı yöndeki katılımcılar, oluşturucu son yükün şifresini çözene kadar şifrelemeye devam eder.
- **Outbound tunnels:** ağ geçidi, her atlamanın şifrelemesinin tersini önceden uygular; böylece her katılımcı şifreler. Uç nokta şifrelediğinde, ağ geçidinin asıl açık metni ortaya çıkar.

Her iki yön de `{tunnelId, IV, encryptedPayload}` verisini bir sonraki atlama noktasına iletir.

---

## Tunnel Mesaj Biçimi {#tunnel-message-format}

tunnel ağ geçitleri, payload (taşınan veri) uzunluğunu gizlemek ve per-hop (her atlama) işlemeyi basitleştirmek için I2NP iletilerini sabit boyutlu zarflara böler.

### Şifrelenmiş Yerleşim {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – Sonraki atlama için 32 bitlik tanımlayıcı (sıfır olmayan, her oluşturma döngüsünde değişir).
- **IV** (başlatma vektörü) – Her mesaj için seçilen 16 baytlık AES IV.
- **Şifrelenmiş yük** – 1008 baytlık AES-256-CBC şifreli metin.

Toplam boyut: 1028 bayt.

### Şifresi Çözülmüş Yerleşim {#decrypted-layout}

Bir hop (ara düğüm), kendi şifreleme katmanını kaldırdıktan sonra:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Sağlama toplamı** şifresi çözülmüş bloğu doğrular.
- **Dolgu** bir sıfır baytla sonlandırılan rastgele sıfır olmayan baytlardır.
- **Teslim talimatları** uç noktaya her parçanın nasıl ele alınacağını söyler (yerel olarak teslim etme, başka bir tunnel’a iletme vb.).
- **Parçalar** altta yatan I2NP iletilerini taşır; uç nokta, bunları daha yüksek katmanlara iletmeden önce yeniden birleştirir.

### İşleme Adımları {#processing-steps}

1. Ağ geçitleri I2NP iletilerini parçalara ayırır ve kuyruğa alır, yeniden birleştirme için kısmi parçaları kısa süreliğine tutar.
2. Ağ geçidi yükü uygun katman anahtarlarıyla şifreler ve tunnel ID ile IV'yi ekler.
3. Her katılımcı IV'yi (AES-256/ECB) ve ardından yükü (AES-256/CBC) şifreler, sonra IV'yi yeniden şifreleyip iletiyi iletir.
4. Uç nokta ters sırada şifreyi çözer, sağlama toplamını doğrular, teslimat talimatlarını işler ve parçaları yeniden birleştirir.

---

## Tunnel Oluşturma (ECIES-X25519) {#tunnel-creation-ecies}

Modern router'lar, ECIES-X25519 anahtarlarıyla tunnel kurar; bu, oluşturma mesajlarını küçültür ve ileri gizlilik sağlar.

- **Build message:** tek bir `TunnelBuild` (veya `VariableTunnelBuild`) I2NP mesajı, her atlama için bir tane olmak üzere 1–8 şifreli oluşturma kaydı taşır.
- **Layer keys:** oluşturucular, atlama başına katman, IV ve yanıt anahtarlarını, atlamanın statik X25519 kimliği ve oluşturucunun geçici anahtarı kullanılarak HKDF ile türetir.
- **Processing:** her atlama kendi kaydının şifresini çözer, istek bayraklarını doğrular, yanıt bloğunu yazar (başarı ya da ayrıntılı hata kodu), kalan kayıtları yeniden şifreler ve mesajı iletir.
- **Replies:** oluşturucu, garlic (I2P'de birden çok mesajın tek bir şifreli kapsülde paketlenmesi tekniği) ile paketlenmiş bir yanıt mesajı alır. Hatalı olarak işaretlenen kayıtlar, router'ın eşi profilleyebilmesi için bir ciddiyet kodu içerir.
- **Compatibility:** router'lar geriye dönük uyumluluk için hâlâ eski ElGamal oluşturma yöntemlerini kabul edebilir, ancak yeni tunnel'ler varsayılan olarak ECIES kullanır.

> Alan bazında sabitler ve anahtar türetme notları için, ECIES (Eliptik Eğri Tümleşik Şifreleme Şeması) öneri geçmişine ve router kaynak koduna bakın; bu kılavuz çalışma akışını kapsar.

---

## Eski Tunnel Oluşturma (ElGamal-2048) {#tunnel-creation-elgamal}

İlk tunnel oluşturma biçimi ElGamal açık anahtarlarını kullanıyordu. Modern routers, geriye dönük uyumluluk için sınırlı destek sağlamaya devam eder.

> **Durum:** Kullanımdan kaldırılmıştır. Tarihsel referans amacıyla ve geriye dönük uyumlu araçların bakımını yapanlar için burada tutulmaktadır.

- **Non-interactive telescoping (etkileşimsiz teleskoplama):** tek bir oluşturma iletisi tüm yolu geçer. Her atlama kendi 528 baytlık kaydını çözer, iletiyi günceller ve iletir.
- **Değişken uzunluk:** Variable Tunnel Build Message (VTBM) (değişken tunnel oluşturma iletisi) 1–8 kayda izin verirdi. Daha önceki sabit ileti, tunnel uzunluğunu gizlemek için her zaman sekiz kayıt içeriyordu.
- **İstek kayıt düzeni:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Bayraklar:** 7. bit bir inbound gateway (gelen ağ geçidi) (IBGW) olduğunu belirtir; 6. bit bir outbound endpoint (giden uç nokta) (OBEP) olduğunu işaretler. Bunlar birbirini dışlar.
- **Şifreleme:** her kayıt, atlamanın açık anahtarıyla ElGamal-2048 kullanılarak şifrelenir. Simetrik AES-256-CBC katmanlaması, yalnızca hedeflenen atlamanın kendi kaydını okuyabilmesini sağlar.
- **Temel bilgiler:** tunnel ID'leri sıfır olmayan 32 bit değerlerdir; oluşturucular, gerçek tunnel uzunluğunu gizlemek için sahte kayıtlar ekleyebilir; güvenilirlik, başarısız oluşturma işlemlerini yeniden denemeye bağlıdır.

---

## Tunnel Havuzları ve Yaşam Döngüsü {#tunnel-pools}

Routers, keşif trafiği ve her bir I2CP oturumu için birbirinden bağımsız gelen ve giden tunnel havuzları yönetir.

- **Eş seçimi:** exploratory tunnels çeşitliliği teşvik etmek için “active, not failing” eş kovasından seçim yapar; client tunnels ise hızlı, yüksek kapasiteli eşleri tercih eder.
- **Deterministik sıralama:** eşler, `SHA256(peerHash || poolKey)` ile havuzun rastgele anahtarı arasındaki XOR mesafesine göre sıralanır. Anahtar, yeniden başlatıldığında döner; bu da tek bir çalıştırma içinde istikrar sağlarken farklı çalıştırmalar arasında öncül saldırılarını zorlaştırır.
- **Yaşam döngüsü:** routers, `{mode, direction, length, variance}` demetine (tuple) göre geçmiş kurma sürelerini izler. tunnels sona ermeye yaklaştıkça, yerlerini alacak olanlar erken başlatılır; router, başarısızlıklar olduğunda paralel kurma sayısını artırırken bekleyen deneme sayısını sınırlar.
- **Yapılandırma ayarları:** etkin/yedek tunnel sayıları, atlama (hop) uzunluğu ve varyansı, sıfır-atlama izinleri ve kurma hız limitleri, havuz başına ayarlanabilir.

---

## Tıkanıklık ve Güvenilirlik {#congestion}

Her ne kadar tunnels devrelere benzese de, routers onları mesaj kuyrukları olarak ele alır. Weighted Random Early Discard (WRED) (Ağırlıklı Rastgele Erken Atma), gecikmeyi sınırlı tutmak için kullanılır:

- Düşürme olasılığı, kullanım yapılandırılmış sınırlara yaklaştıkça artar.
- Katılımcılar sabit boyutlu parçaları dikkate alır; ağ geçitleri/uç noktaları birleşik parça boyutuna göre düşürür, önce büyük yükleri düşürür.
- En az ağ çabası boşa gitsin diye, giden uç noktalar diğer rollerden önce düşürür.

Garantili teslimat, [Streaming library](/docs/specs/streaming/) (akış kütüphanesi) gibi daha üst katmanlara bırakılmıştır. Güvenilirlik gerektiren uygulamalar, yeniden iletim ve onayları kendileri yönetmelidir.

---

## Daha Fazla Okuma {#further-reading}

- [Eş Seçimi](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel Genel Bakışı](/docs/overview/tunnel-routing/)
- [Eski Tunnel Gerçeklemesi](/docs/legacy/old-implementation/)
