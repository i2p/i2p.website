---
title: "I2P İstemci Protokolü (I2CP)"
description: "Uygulamalar, I2P router ile oturumları, tunnels ve LeaseSets'i nasıl müzakere eder."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

I2CP, bir I2P router ile herhangi bir istemci süreci arasındaki alt düzey kontrol protokolüdür. Sorumlulukların katı bir ayrımını tanımlar:

- **Router**: Yönlendirmeyi, kriptografiyi, tunnel yaşam döngülerini ve ağ veritabanı işlemlerini yönetir
- **İstemci**: Anonimlik özelliklerini seçer, tunnel'ları yapılandırır ve iletiler gönderir/alır

Tüm iletişim tek bir TCP soketi (isteğe bağlı olarak TLS ile sarmalanmış) üzerinden gerçekleşir; bu da eşzamansız, tam çift yönlü işlemleri mümkün kılar.

**Protokol Sürümü**: I2CP, ilk bağlantı kurulumu sırasında gönderilen `0x2A` (ondalık olarak 42) değerindeki bir protokol sürüm baytı kullanır. Bu sürüm baytı, protokolün başlangıcından beri sabit kalmıştır.

**Güncel Durum**: Bu spesifikasyon, 2025-09'da yayımlanan router sürümü 0.9.67 (API sürümü 0.9.67) için geçerlidir.

## Uygulama Bağlamı

### Java Implementasyonu

Başvuru uygulaması Java I2P'de bulunur: - İstemci SDK'sı: `i2p.jar` paketi - Router gerçekleştirmesi: `router.jar` paketi - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

İstemci ve router aynı JVM'de çalıştığında, I2CP mesajları serileştirme olmadan Java nesneleri olarak aktarılır. Harici istemciler TCP üzerinden serileştirilmiş protokolü kullanır.

### C++ Gerçeklemesi

i2pd (C++ I2P router) ayrıca istemci bağlantıları için I2CP'yi harici olarak uygular.

### Java Olmayan İstemciler

Eksiksiz bir I2CP istemci kitaplığının **bilinen Java dışı implementasyonları yoktur**. Java dışı uygulamalar bunun yerine daha üst düzey protokolleri kullanmalıdır:

- **SAM (Simple Anonymous Messaging) v3**: Birden çok dilde kütüphaneleri bulunan soket tabanlı bir arayüz
- **BOB (Basic Open Bridge)**: SAM'e daha basit bir alternatif

Bu daha üst düzey protokoller, I2CP karmaşıklığını kendi içinde yönetir ve ayrıca akış kitaplığını (TCP benzeri bağlantılar için) ve datagram kitaplığını (UDP benzeri bağlantılar için) sağlar.

## Bağlantı Kurulumu

### 1. TCP Bağlantısı

router I2CP bağlantı noktasına bağlanın: - Varsayılan: `127.0.0.1:7654` - router ayarları üzerinden yapılandırılabilir - İsteğe bağlı TLS sarmalayıcı (uzak bağlantılar için şiddetle önerilir)

### 2. Protokol El Sıkışması

**Adım 1**: Protokol sürüm baytını `0x2A` gönderin

**Adım 2**: Saat Senkronizasyonu

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
router, kendi geçerli zaman damgasını ve I2CP API sürüm dizesini döndürür (0.8.7'den beri).

**Adım 3**: Kimlik doğrulama (etkinleştirildiyse)

0.9.11 itibarıyla, kimlik doğrulama, şunları içeren bir Mapping (eşleme) aracılığıyla GetDateMessage (tarih alma mesajı) içine eklenebilir: - `i2cp.username` - `i2cp.password`

0.9.16 sürümünden itibaren, kimlik doğrulama etkinleştirildiğinde, diğer herhangi bir mesaj gönderilmeden önce GetDateMessage aracılığıyla tamamlanması **zorunludur**.

**Adım 4**: Oturum Oluşturma

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Adım 5**: Tunnel Hazır Sinyali

```
Router → Client: RequestVariableLeaseSetMessage
```
Bu mesaj, gelen tunnel'ların oluşturulduğunu bildirir. router, en az bir gelen VE bir giden tunnel mevcut olana kadar bunu GÖNDERMEYECEKTİR.

**Adım 6**: LeaseSet Yayınlanması

```
Client → Router: CreateLeaseSet2Message
```
Bu noktada, oturum mesaj gönderme ve alma için tamamen işler durumdadır.

## Mesaj Akış Kalıpları

### Giden Mesaj (İstemci uzak hedefe gönderir)

**i2cp.messageReliability=none ile**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**i2cp.messageReliability=BestEffort ile**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Gelen İleti (Router istemciye iletir)

**i2cp.fastReceive=true ile** (0.9.4'ten beri varsayılan):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**i2cp.fastReceive=false ile** (KULLANIMDAN KALDIRILDI):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Modern istemciler her zaman hızlı alım modunu kullanmalıdır.

## Yaygın Veri Yapıları

### I2CP Mesaj Başlığı

Tüm I2CP mesajları bu ortak başlığı kullanır:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Gövde Uzunluğu**: 4 baytlık tamsayı, yalnızca mesaj gövdesinin uzunluğu (başlığı içermez)
- **Tür**: 1 baytlık tamsayı, mesaj türü tanımlayıcısı
- **Mesaj Gövdesi**: 0+ bayt, biçim mesaj türüne göre değişir

**Mesaj Boyutu Sınırı**: En fazla yaklaşık 64 KB.

### Oturum Kimliği

Bir router üzerinde bir oturumu benzersiz şekilde tanımlayan 2 baytlık tamsayı.

**Özel Değer**: `0xFFFF` "oturum yok" anlamına gelir (kurulmuş bir oturum olmadan yapılan ana bilgisayar adı sorguları için kullanılır).

### Mesaj Kimliği

Bir oturum içindeki bir mesajı benzersiz olarak tanımlamak için router tarafından oluşturulan 4 baytlık tamsayı.

**Önemli**: Mesaj kimlikleri küresel olarak benzersiz **değildir**, yalnızca bir oturum içinde benzersizdir. Ayrıca, istemci tarafından üretilen nonce'tan (tek kullanımlık sayı) farklıdır.

### Yük Biçimi

Mesaj yükleri, standart 10 baytlık bir gzip üstbilgisiyle gzip sıkıştırılır: - Şununla başlar: `0x1F 0x8B 0x08` (RFC 1952) - 0.7.1'den beri: gzip üstbilgisinin kullanılmayan bölümleri protokol, kaynak bağlantı noktası ve hedef bağlantı noktası bilgilerini içerir - Bu, aynı hedef üzerinde hem akış hem de datagramları mümkün kılar

**Sıkıştırma Kontrolü**: Sıkıştırmayı devre dışı bırakmak için `i2cp.gzip=false` olarak ayarlayın (gzip çaba düzeyini 0’a ayarlar). gzip başlığı yine de dahil edilir, ancak sıkıştırma ek yükü asgaridir.

### SessionConfig Yapısı

İstemci oturumu yapılandırmasını tanımlar:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Kritik Gereksinimler**: 1. **Eşleme anahtara göre sıralanmış olmalıdır** imza doğrulaması için 2. **Oluşturma Tarihi** router'ın mevcut zamanına göre ±30 saniye içinde olmalıdır 3. **İmza** Destination'ın SigningPrivateKey'i tarafından oluşturulur

**Çevrimdışı İmzalar** (0.9.38 itibarıyla):

Çevrimdışı imzalama kullanılıyorsa, Eşleme şunları içermelidir: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

Ardından Signature, geçici SigningPrivateKey tarafından oluşturulur.

## Çekirdek Yapılandırma Seçenekleri

### Tunnel Yapılandırması

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Notlar**: - `quantity` için 6'dan büyük değerler 0.9.0+ çalıştıran eşler gerektirir ve kaynak kullanımını önemli ölçüde artırır - Yüksek erişilebilirlikli hizmetler için `backupQuantity` değerini 1-2 olarak ayarlayın - Sıfır atlamalı tunnels daha düşük gecikme için anonimliği feda eder ancak test için kullanışlıdır

### Mesaj İşleme

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Mesaj Güvenilirliği**: - `None`: Router alındı onayı göndermez (0.8.1'den beri akış kitaplığının varsayılanı) - `BestEffort`: Router kabul + başarı/başarısızlık bildirimleri gönderir - `Guaranteed`: Uygulanmadı (şu anda BestEffort gibi davranır)

**Mesaj Başına Geçersiz Kılma** (0.9.14 sürümünden beri): - `messageReliability=none` olan bir oturumda, sıfır olmayan bir nonce (bir kez kullanılan sayı) ayarlamak, o belirli mesaj için teslim bildirimi talep eder - `BestEffort` oturumunda nonce=0 ayarlamak, o mesaj için bildirimleri devre dışı bırakır

### LeaseSet Yapılandırması

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Eski ElGamal/AES Oturum Etiketleri

Bu seçenekler yalnızca eski ElGamal şifrelemesi için geçerlidir:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Not**: ECIES-X25519 istemcileri farklı bir ratchet (ardışık anahtar yenileme) mekanizması kullanır ve bu seçenekleri yok sayar.

## Şifreleme Türleri

I2CP, `i2cp.leaseSetEncType` seçeneği aracılığıyla birden fazla uçtan uca şifreleme şemasını destekler. Hem modern hem de eski eşleri desteklemek için birden fazla tür belirtilebilir (virgülle ayrılmış).

### Desteklenen Şifreleme Türleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Önerilen Yapılandırma**:

```
i2cp.leaseSetEncType=4,0
```
Bu, uyumluluk amacıyla ElGamal geri dönüş mekanizmasıyla birlikte X25519’u (tercih edilen) sağlar.

### Şifreleme Türü Ayrıntıları

**Type 0 - ElGamal/AES+SessionTags**: - 2048-bit ElGamal açık anahtarlar (256 bayt) - AES-256 simetrik şifreleme - toplu olarak gönderilen 32 baytlık oturum etiketleri - yüksek CPU, bant genişliği ve bellek ek yükü - ağ genelinde aşamalı olarak kullanımdan kaldırılıyor

**Tip 4 - ECIES-X25519-AEAD-Ratchet**: - X25519 anahtar değişimi (32 baytlık anahtarlar) - ChaCha20/Poly1305 AEAD (ilişkili verili kimlik doğrulamalı şifreleme) - Signal tarzı double ratchet (çift kademeli anahtar yenileme mekanizması) - 8 bayt oturum etiketleri (ElGamal için 32 bayta karşılık) - Etiketler senkronize PRNG (sözde rastgele sayı üreteci) aracılığıyla üretilir (önceden gönderilmez) - ElGamal’a kıyasla ~92% ek yük azaltımı - Modern I2P için standarttır (çoğu router bunu kullanır)

**Tip 5-6 - Kuantum Sonrası Hibrit**: - X25519 ile ML-KEM'i birleştirir (NIST FIPS 203) - Kuantuma dayanıklı güvenlik sağlar - Dengeli güvenlik/performans için ML-KEM-768 - Maksimum güvenlik için ML-KEM-1024 - PQ anahtar materyali (post-quantum; kuantum sonrası) nedeniyle daha büyük mesaj boyutları - Ağ desteği hâlen devreye alınıyor

### Geçiş Stratejisi

I2P ağı, ElGamal (tip 0)'dan X25519 (tip 4)'e aktif olarak geçiş yapıyor: - NTCP → NTCP2 (tamamlandı) - SSU → SSU2 (tamamlandı) - ElGamal tunnels → X25519 tunnels (tamamlandı) - ElGamal uçtan uca → ECIES-X25519 (büyük ölçüde tamamlandı)

## LeaseSet2 ve Gelişmiş Özellikler

### LeaseSet2 Seçenekleri (0.9.38'den beri)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Körlenmiş Adresler

0.9.39 itibarıyla, hedefler periyodik olarak değişen "blinded" (körlenmiş) adresleri (b33 biçimi) kullanabilir: - Parola koruması için `i2cp.leaseSetSecret` gerektirir - İsteğe bağlı istemci başına kimlik doğrulama - Ayrıntılar için 123 ve 149 numaralı önerilere bakın

### Hizmet Kayıtları (0.9.66 sürümünden beri)

LeaseSet2 servis kaydı seçeneklerini destekler (öneri 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Biçim, DNS SRV kayıt biçimini izler ancak I2P'ye uyarlanmıştır.

## Birden Çok Oturum (0.9.21'den beri)

Tek bir I2CP bağlantısı birden fazla oturumu destekleyebilir:

**Birincil Oturum**: Bir bağlantıda oluşturulan ilk oturum **Alt Oturumlar**: Birincil oturumun tunnel havuzunu paylaşan ek oturumlar

### Subsession (alt oturum) Özellikleri

1. **Paylaşılan Tunnels**: Birincil ile aynı gelen/giden tunnel havuzlarını kullanın
2. **Paylaşılan Şifreleme Anahtarları**: Özdeş LeaseSet şifreleme anahtarlarını kullanmalıdır
3. **Farklı İmzalama Anahtarları**: Ayrı Destination (I2P'de hedef kimlik) imzalama anahtarları kullanmalıdır
4. **Anonimlik Garantisi Yok**: Birincil oturumla açıkça bağlantılıdır (aynı router, aynı tunnels)

### Subsession (alt oturum) kullanım senaryosu

Farklı imza türleri kullanan hedeflerle iletişimi etkinleştirin: - Birincil: EdDSA imzası (modern) - Subsession (alt oturum): DSA imzası (eski sürümlerle uyumluluk)

### Alt Oturum Yaşam Döngüsü

**Oluşturma**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Sonlandırma**: - Alt oturumu sonlandırmak: Birincil oturum bozulmadan kalır - Birincil oturumu sonlandırmak: Tüm alt oturumları sonlandırır ve bağlantıyı kapatır - DisconnectMessage (bağlantıyı kesme mesajı): Tüm oturumları sonlandırır

### Oturum Kimliği Yönetimi

Çoğu I2CP mesajı bir Oturum Kimliği alanı içerir. İstisnalar: - DestLookup / DestReply (kullanımdan kaldırıldı, HostLookup / HostReply kullanın) - GetBandwidthLimits / BandwidthLimits (yanıt oturuma özgü değildir)

**Önemli**: İstemciler, yanıt bekleyen birden fazla CreateSession mesajını aynı anda bulundurmamalıdır; çünkü yanıtlar isteklerle kesin olarak ilişkilendirilemez.

## Mesaj Kataloğu

### Mesaj Türleri Özeti

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Açıklama**: C = İstemci, R = Router

### Anahtar Mesaj Ayrıntıları

#### CreateSessionMessage (Oturum Oluşturma Mesajı) (Tür 1)

**Amaç**: Yeni bir I2CP (I2P'nin İstemci Protokolü) oturumu başlatmak

**İçerik**: SessionConfig yapısı

**Yanıt**: SessionStatusMessage (status=Created veya Invalid)

**Gereksinimler**: - SessionConfig (oturum yapılandırması) içindeki tarih, router saatine göre ±30 saniye içinde olmalıdır - İmza doğrulaması için eşleme anahtara göre sıralanmış olmalıdır - Destination (hedef) zaten etkin bir oturuma sahip olmamalıdır

#### RequestVariableLeaseSetMessage (Tür 37)

**Amaç**: Router, gelen tunnels için istemci yetkilendirmesi ister

**İçerik**: - Oturum Kimliği - Lease sayısı (Lease: sona erme zamanı olan erişilebilirlik kaydı) - Lease yapılarından oluşan dizi (her birinin kendi sona erme zamanı vardır)

**Yanıt**: CreateLeaseSet2Message

**Önemi**: Bu, oturumun çalışır durumda olduğunu belirten sinyaldir. router bunu yalnızca şu durumların ardından gönderir: 1. En az bir inbound tunnel kuruldu 2. En az bir outbound tunnel kuruldu

**Zaman Aşımı Önerisi**: Bu mesaj, oturum oluşturulduktan sonra 5+ dakika içinde alınmazsa istemciler oturumu sonlandırmalıdır.

#### CreateLeaseSet2Message (Tür 41)

**Amaç**: İstemci LeaseSet'i ağ veritabanına yayınlar

**İçerik**: - Oturum Kimliği - LeaseSet (kiralama kümesi) tip baytı (1, 3 veya 7) - LeaseSet veya LeaseSet2 veya EncryptedLeaseSet veya MetaLeaseSet - Özel anahtar sayısı - Özel anahtar listesi (LeaseSet içindeki her açık anahtar için bir tane, aynı sırada)

**Özel Anahtarlar**: Gelen garlic messages (I2P'nin garlic encryption tekniğiyle paketlenen iletiler) şifrelerini çözmek için gereklidir. Biçim:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Not**: Aşağıdakileri desteklemeyen kullanımdan kaldırılmış CreateLeaseSetMessage (tip 4)'in yerini alır: - LeaseSet2 varyantları (I2P'de bir hedefin erişim bilgilerini içeren kayıt) - ElGamal dışı şifreleme - Birden fazla şifreleme türü - Şifrelenmiş LeaseSet'ler - Çevrimdışı imzalama anahtarları

#### SendMessageExpiresMessage (Tip 36)

**Amaç**: Mesajı geçerlilik süresi ve gelişmiş seçeneklerle hedefe gönder

**İçerik**: - Oturum Kimliği - Hedef - Yük (gzip ile sıkıştırılmış) - Nonce (tek kullanımlık sayı, 4 bayt) - Bayraklar (2 bayt) - aşağıya bakın - Sona Erme Tarihi (6 bayt, 8 bayttan kısaltılmış)

**Flags Alanı** (2 bayt, bit sırası 15...0):

**Bitler 15-11**: Kullanılmıyor, 0 olmalıdır

**Bitler 10-9**: Mesaj Güvenilirliği Geçersiz Kılma (kullanılmıyor, bunun yerine nonce (tek seferlik sayı) kullanın)

**Bit 8**: LeaseSet'i paketleme - 0: Router, LeaseSet'i garlic (I2P'de kullanılan garlic encryption) içinde paketleyebilir - 1: LeaseSet'i paketleme

**Bitler 7-4**: Düşük etiket eşiği (yalnızca ElGamal, ECIES için yok sayılır)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bits 3-0**: Gerekirse gönderilecek etiketler (yalnızca ElGamal için, ECIES için yok sayılır)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Tür 22)

**Amaç**: İletinin teslim durumunu istemciye bildirmek

**İçerik**: - Oturum Kimliği - Mesaj Kimliği (router tarafından oluşturulan) - Durum kodu (1 bayt) - Boyut (4 bayt, yalnızca status=0 için geçerlidir) - Nonce (4 bayt, istemcinin SendMessage nonce'u ile eşleşir)

**Durum Kodları** (Giden Mesajlar):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Başarı kodları**: 1, 2, 4, 6 **Hata kodları**: Geri kalanların tümü

**Durum Kodu 0** (KULLANIMDAN KALDIRILDI): Mevcut mesaj (gelen, hızlı alım devre dışı)

#### HostLookupMessage (konak adı sorgu mesajı) (Tip 38)

**Amaç**: Konak adı veya hash ile hedef arama (DestLookup'un yerini alır)

**İçerik**: - Oturum Kimliği (veya oturum yoksa 0xFFFF) - İstek Kimliği (4 bayt) - Zaman aşımı milisaniye cinsinden (4 bayt, önerilen minimum: 10000) - İstek türü (1 bayt) - Arama anahtarı (Hash, hostname String veya Destination)

**İstek Türleri**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
2-4 numaralı tipler, mevcutsa LeaseSet seçeneklerini (öneri 167) döndürür.

**Yanıt**: HostReplyMessage (Ana Makine Yanıt Mesajı)

#### HostReplyMessage (Tür 39)

**Amaç**: HostLookupMessage (konak adı sorgulama mesajı) için yanıt

**İçerik**: - Oturum Kimliği - İstek Kimliği - Sonuç kodu (1 bayt) - Hedef (başarılı olduğunda mevcut, bazen belirli başarısızlık durumlarında) - Eşleme (yalnızca arama türleri 2-4 için, boş olabilir)

**Sonuç Kodları**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (Tür 42)

**Amaç**: router'a blinded destination (körleştirilmiş hedef) kimlik doğrulama gereksinimleri hakkında bilgi vermek (0.9.43'ten beri)

**İçerik**: - Oturum Kimliği - Bayraklar (1 bayt) - Uç nokta türü (1 bayt): 0=Hash, 1=hostname, 2=Destination, 3=SigType+Key - Kör imza türü (2 bayt) - Sona erme zamanı (4 bayt, epoch'tan beri geçen saniyeler) - Uç nokta verisi (türe göre değişir) - Özel anahtar (32 bayt, yalnızca bayrak biti 0 ayarlıysa) - Arama parolası (String, yalnızca bayrak biti 4 ayarlıysa)

**Bayraklar** (bit sırası 76543210):

- **Bit 0**: 0=herkes, 1=istemci başına
- **Bitler 3-1**: Kimlik doğrulama şeması (bit 0=1 ise): 000=DH, 001=PSK
- **Bit 4**: 1=sır gerekli
- **Bitler 7-5**: Kullanılmıyor, 0'a ayarlayın

**Yanıt yok**: Router sessizce işlem yapar

**Kullanım Senaryosu**: Bir blinded destination (b33 address - gizlenmiş hedef) adresine göndermeden önce, istemci şunlardan birini yapmalıdır: 1. b33'ü HostLookup (ana bilgisayar adı çözümlemesi) aracılığıyla çözümlemek, VEYA 2. BlindingInfo message (körleştirme bilgisi iletisi) göndermek

Hedef kimlik doğrulama gerektiriyorsa, BlindingInfo zorunludur.

#### ReconfigureSessionMessage (Tip 2)

**Amaç**: Oluşturma sonrasında oturum yapılandırmasını güncellemek

**İçerik**: - Session ID - SessionConfig (yalnızca değiştirilen seçenekler gerekli)

**Yanıt**: SessionStatusMessage (status=Updated veya Invalid)

**Notlar**: - Router yeni yapılandırmayı mevcut yapılandırmayla birleştirir - Tunnel seçenekleri (`inbound.*`, `outbound.*`) her zaman uygulanır - Bazı seçenekler oturum oluşturulduktan sonra değiştirilemez olabilir - Tarih, router saatinin ±30 saniyesi içinde olmalıdır - Eşleme anahtara göre sıralanmış olmalıdır

#### DestroySessionMessage (oturumu yok etme mesajı) (Tip 3)

**Amaç**: Bir oturumu sonlandırmak

**İçerik**: Oturum Kimliği

**Beklenen Yanıt**: SessionStatusMessage (status=Destroyed)

**Gerçek Davranış** (Java I2P 0.9.66'ya kadar): - Router asla SessionStatus(Destroyed) göndermez - Hiç oturum kalmamışsa: DisconnectMessage gönderir - Alt oturumlar kalmışsa: Yanıt yok

**Önemli**: Java I2P'nin davranışı spesifikasyondan sapmaktadır. Gerçekleştirimler, tek tek subsessions (alt oturumlar) sonlandırılırken dikkatli olmalıdır.

#### DisconnectMessage (Tür 30)

**Amaç**: Bağlantının sonlandırılmak üzere olduğunu bildirmek

**İçerik**: Gerekçe Dizesi

**Etkisi**: Bağlantıdaki tüm oturumlar sonlandırılır, soket kapanır

**Gerçekleme**: Ağırlıklı olarak Java I2P'de router → istemci

## Protokol Sürüm Geçmişi

### Sürüm Tespiti

I2CP protokol sürümü, Get/SetDate mesajlarında alınıp verilir (0.8.7'den beri). Daha eski routers için sürüm bilgisi mevcut değildir.

**Sürüm Dizesi**: "core" (çekirdek) API sürümünü belirtir, router sürümünü belirtmek zorunda değildir.

### Özellik Zaman Çizelgesi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Güvenlik Hususları

### Kimlik Doğrulama

**Varsayılan**: Kimlik doğrulama gerekmez **İsteğe bağlı**: Kullanıcı adı/şifre ile kimlik doğrulama (0.9.11 sürümünden beri) **Zorunlu**: Etkinleştirildiğinde, diğer mesajlardan önce kimlik doğrulamanın tamamlanması gerekir (0.9.16 sürümünden beri)

**Uzaktan Bağlantılar**: Kimlik bilgilerini ve özel anahtarları korumak için her zaman TLS (`i2cp.SSL=true`) kullanın.

### Saat Kayması

SessionConfig Date, router saatinden ±30 saniye içinde olmalıdır; aksi halde oturum reddedilecektir. Senkronize etmek için Get/SetDate kullanın.

### Özel Anahtar Yönetimi

CreateLeaseSet2Message, gelen mesajların şifresini çözmek için özel anahtarlar içerir. Bu anahtarlar şu şekilde olmalıdır: - Güvenli şekilde iletilmelidir (uzak bağlantılar için TLS) - router tarafından güvenli şekilde saklanmalıdır - Kompromize olduğunda yenilenmelidir

### Mesajın Sona Ermesi

Açık bir sona erme süresi belirlemek için her zaman SendMessageExpires (SendMessage değil) kullanın. Bu:
- İletilerin süresiz olarak kuyruğa alınmasını engeller
- Kaynak tüketimini azaltır
- Güvenilirliği artırır

### Oturum Etiketi Yönetimi

**ElGamal** (kullanımdan kaldırılmış): - Etiketler toplu olarak iletilmelidir - Kaybolan etiketler şifre çözme hatalarına neden olur - Yüksek bellek ek yükü

**ECIES-X25519** (mevcut): - Senkronize PRNG (sözde rastgele sayı üreteci) ile üretilen etiketler - Önceden gönderim gerekmez - Mesaj kaybına dayanıklı - Önemli ölçüde daha düşük ek yük

## En İyi Uygulamalar

### İstemci Geliştiriciler için

1. **Hızlı Alma Modunu Kullanın**: Her zaman `i2cp.fastReceive=true` olarak ayarlayın (veya varsayılanı kullanın)

2. **ECIES-X25519'i tercih edin**: Uyumluluğu korurken en iyi performans için `i2cp.leaseSetEncType=4,0` ayarını yapılandırın

3. **Sona Erme Süresini Açıkça Belirleyin**: SendMessageExpires kullanın, SendMessage değil

4. **Subsessions (alt oturumlar) dikkatle ele alın**: subsessions hedefler arasında anonimlik sağlamaz; bunun farkında olun

5. **Oturum Oluşturma Zaman Aşımı**: RequestVariableLeaseSet (değişken leaseSet isteği) 5 dakika içinde alınmazsa oturumu sonlandır

6. **Yapılandırma Eşlemelerini Sırala**: SessionConfig'i imzalamadan önce eşleme anahtarlarını her zaman sıralayın

7. **Uygun Tunnel Sayılarını Kullanın**: Gerekli olmadıkça `quantity` > 6 olarak ayarlamayın

8. **Java dışı için SAM/BOB (I2P istemci arayüzü protokolleri) kullanmayı değerlendirin**: Doğrudan I2CP'yi uygulamak yerine SAM'i uygulayın

### Router Geliştiricileri için

1. **Tarihleri Doğrulayın**: SessionConfig tarihlerinde ±30 saniyelik bir zaman penceresini uygulayın

2. **Mesaj Boyutunu Sınırla**: ~64 KB maksimum mesaj boyutunu zorunlu tut

3. **Birden Çok Oturumu Destekleyin**: 0.9.21 belirtimine göre subsession (alt oturum) desteğini uygulayın

4. **RequestVariableLeaseSet gönderimini gecikmeden yapın**: Yalnızca hem inbound hem de outbound tunnels mevcut olduktan sonra

5. **Kullanımdan Kaldırılmış Mesajları Ele Alın**: ReceiveMessageBegin/End'i kabul edin ancak kullanımını caydırın

6. **ECIES-X25519'i destekleyin**: Yeni dağıtımlar için tip 4 şifrelemeye öncelik verin (X25519 eğrisi kullanan ECIES şifreleme)

## Hata Ayıklama ve Sorun Giderme

### Yaygın Sorunlar

**Oturum Reddedildi (Geçersiz)**: - Saat sapmasını kontrol edin (±30 saniye içinde olmalı) - Mapping (eşleştirme) anahtara göre sıralı mı, doğrulayın - Destination (hedef) halihazırda kullanımda olmadığından emin olun

**RequestVariableLeaseSet yok**: - Router tunnel oluşturuyor olabilir (en fazla 5 dakika bekleyin) - Ağ bağlantı sorunları olup olmadığını kontrol edin - Yeterli eş bağlantısı olduğunu doğrulayın

**Mesaj İletim Hataları**: - Belirli başarısızlık nedenini belirlemek için MessageStatus (mesaj durumu) kodlarını kontrol edin - Uzak LeaseSet'in yayımlandığını ve güncel olduğunu doğrulayın - Uyumlu şifreleme türlerinin kullanıldığından emin olun

**Subsession (alt oturum) Sorunları**: - Önce birincil oturumun oluşturulduğunu doğrulayın - Aynı şifreleme anahtarlarının kullanıldığını doğrulayın - İmzalama anahtarlarının farklı olduğunu kontrol edin

### Tanılama Mesajları

**GetBandwidthLimits**: router kapasitesini sorgulayın **HostLookup**: ad çözümlemesini ve LeaseSet kullanılabilirliğini test edin **MessageStatus**: mesaj teslimatını uçtan uca izleyin

## İlgili Spesifikasyonlar

- **Ortak Yapılar**: /docs/specs/common-structures/
- **I2NP (Ağ Protokolü)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Tunnel Oluşturma**: /docs/specs/implementation/
- **Akış Kitaplığı**: /docs/specs/streaming/
- **Datagram Kitaplığı**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Atıfta Bulunulan Öneriler

- [Öneri 123](/proposals/123-new-netdb-entries/): Şifrelenmiş LeaseSet'ler ve kimlik doğrulama
- [Öneri 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Öneri 149](/proposals/149-b32-encrypted-ls2/): Körleştirilmiş adres biçimi (b33)
- [Öneri 152](/proposals/152-ecies-tunnels/): X25519 tunnel oluşturma
- [Öneri 154](/proposals/154-ecies-lookups/): ECIES hedeflerinden veritabanı sorguları
- [Öneri 156](/proposals/156-ecies-routers/): Router'ın ECIES-X25519'a geçişi
- [Öneri 161](/tr/proposals/161-ri-dest-padding/): Hedef dolgusu sıkıştırması
- [Öneri 167](/proposals/167-service-records/): LeaseSet hizmet kayıtları
- [Öneri 169](/proposals/169-pq-crypto/): Kuantum-sonrası hibrit kriptografi (ML-KEM)

## Javadocs Referansı

- [I2CP Paketi](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [İstemci API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Kullanımdan Kaldırma Özeti

### Kullanımdan Kaldırılmış Mesajlar (Kullanmayın)

- **CreateLeaseSetMessage** (tip 4): CreateLeaseSet2Message kullanın
- **RequestLeaseSetMessage** (tip 21): RequestVariableLeaseSetMessage kullanın
- **ReceiveMessageBeginMessage** (tip 6): hızlı alma modunu kullanın
- **ReceiveMessageEndMessage** (tip 7): hızlı alma modunu kullanın
- **DestLookupMessage** (tip 34): HostLookupMessage kullanın
- **DestReplyMessage** (tip 35): HostReplyMessage kullanın
- **ReportAbuseMessage** (tip 29): Hiç uygulanmadı

### Kullanımdan Kaldırılmış Seçenekler

- ElGamal şifreleme (type 0): ECIES-X25519'e (type 4) geçin
- DSA imzaları: EdDSA'ya veya ECDSA'ya geçin
- `i2cp.fastReceive=false`: Her zaman hızlı alma modunu kullanın
