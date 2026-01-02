---
title: "Ağ Veritabanı"
description: "I2P'nin dağıtık ağ veritabanının (netDb) anlaşılması - router iletişim bilgileri ve destination (hedef) sorguları için özelleşmiş bir DHT"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Genel Bakış

**netDb**, yalnızca iki tür veri içeren özel amaçlı bir dağıtık veritabanıdır: - **RouterInfos** – router iletişim bilgileri - **LeaseSets** – hedef (destination) iletişim bilgileri

Tüm veriler kriptografik olarak imzalanmıştır ve doğrulanabilir. Her bir kayıt, eskimiş kayıtların düşürülmesi ve güncelliğini yitirmiş olanların yenileriyle değiştirilmesi için liveliness (canlılık durumu) bilgisi içerir; böylece belirli saldırı sınıflarına karşı koruma sağlar.

Dağıtım, **floodfill** (I2P'de dağıtık veritabanını yayan bir mekanizma) kullanır, burada router'ların bir alt kümesi dağıtık veritabanını sürdürür.

---

## 2. RouterInfo

Router'ların diğer router'larla iletişime geçmesi gerektiğinde, şunları içeren **RouterInfo** (router bilgisi) paketlerini değiş tokuş ederler:

- **Router kimliği** – şifreleme anahtarı, imzalama anahtarı, sertifika
- **İletişim adresleri** – router'a nasıl ulaşılacağı
- **Yayımlanma zaman damgası** – bu bilginin ne zaman yayımlandığı
- **Serbest metin seçenekleri** – yetenek bayrakları ve ayarlar
- **Kriptografik imza** – özgünlüğünü kanıtlar

### 2.1 Yetenek Bayrakları

Router'lar kendi RouterInfo'larında harf kodları aracılığıyla yeteneklerini ilan eder:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Bant Genişliği Sınıflandırmaları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Ağ Kimliği Değerleri

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 RouterInfo İstatistikleri

Router'lar ağ analizi için isteğe bağlı sağlık istatistikleri yayınlar: - Exploratory tunnel kurulumunda başarı/ret/zaman aşımı oranları - 1 saatlik ortalama katılımcı tunnel sayısı

İstatistikler `stat_(statname).(statperiod)` biçimini izler ve değerler noktalı virgülle ayrılmıştır.

**Örnek İstatistikler:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router'lar ayrıca şunları da yayınlayabilir: `netdb.knownLeaseSets` ve `netdb.knownRouters`

### 2.5 Aile Seçenekleri

0.9.24 sürümünden itibaren, router'lar aile üyeliğini (aynı operatör) bildirebilir:

- **family**: Aile adı
- **family.key**: İmza türü kodu ile base64 ile kodlanmış imzalama açık anahtarının birleştirilmiş biçimi
- **family.sig**: Aile adının ve 32 baytlık router karmasının imzası

Aynı ailedeki birden fazla router, tek bir tunnel içinde birlikte kullanılmaz.

### 2.6 RouterInfo Zaman Aşımı

- Çalışma süresinin ilk saatinde zaman aşımı yok
- Saklanan RouterInfos (router bilgi kayıtları) 25 veya daha az ise zaman aşımı yok
- Yereldeki sayı arttıkça zaman aşımı süresi kısalır (120'den az router için 72 saat; 300 router için ~30 saat)
- SSU introducers (SSU tanıtıcıları) ~1 saatte zaman aşımına uğrar
- Floodfills tüm yerel RouterInfos için 1 saatlik zaman aşımı kullanır

---

## 3. LeaseSet

**LeaseSets**, belirli hedefler için tunnel giriş noktalarını belgeler ve şunları belirtir:

- **Tunnel ağ geçidi router kimliği**
- **4 baytlık tunnel kimliği**
- **Tunnel sona erme zamanı**

LeaseSets şunları içerir: - **Hedef** – şifreleme anahtarı, imzalama anahtarı, sertifika - **Ek şifreleme açık anahtarı** – uçtan uca garlic encryption için - **Ek imzalama açık anahtarı** – iptal için tasarlanmıştır (şu anda kullanılmıyor) - **Kriptografik imza**

### 3.1 LeaseSet Varyantları

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 LeaseSet'in Süresinin Dolması

Standart LeaseSets (bir destinasyona ulaşmak için yayımlanan erişim kayıtları) içindeki kiraların en geç sona erme zamanında geçersiz hale gelir. LeaseSet2 (LeaseSet’in 2. sürümü) için sona erme zamanı başlıkta belirtilir. EncryptedLeaseSet (şifrelenmiş LeaseSet) ve MetaLeaseSet (birden fazla LeaseSet’i işaret eden meta kayıt) için sona erme süreleri değişebilir; ayrıca olası bir üst sınır uygulanabilir.

---

## 4. Önyükleme

Merkeziyetsiz netDb ağa entegre olabilmek için en az bir eş referansı gerektirir. **Reseeding** (yeniden tohumlama), gönüllülerin netDb dizinlerinden RouterInfo dosyalarını (`routerInfo-$hash.dat`) alır. İlk başlatma sırasında, rastgele seçilen sabit kodlanmış URL’lerden otomatik olarak getirilir.

---

## 5. Floodfill Mekanizması

floodfill netDb basit bir dağıtık depolama kullanır: veri en yakın floodfill eşine gönderilir. floodfill olmayan eşler store iletileri (depolama iletileri) gönderdiğinde, floodfill’ler bunları belirli anahtara en yakın floodfill eşlerinden oluşan bir altkümeye iletir.

Floodfill katılımı, RouterInfo'da bir özellik bayrağı (`f`) olarak belirtilir.

### 5.1 Floodfill'e İsteğe Bağlı Katılım Gereksinimleri

Tor'un sabit kodlu güvenilir dizin sunucularının aksine, I2P'nin floodfill kümesi **güvenilmez** ve zamanla değişir.

Floodfill, yalnızca şu gereksinimleri karşılayan yüksek bant genişliğine sahip router'larda otomatik olarak etkinleşir: - En az 128 KBytes/sec paylaşılan bant genişliği (elle yapılandırılmış) - Ek sağlık testlerini geçmelidir (giden ileti kuyruğu süresi, iş gecikmesi)

Mevcut otomatik katılım, yaklaşık **%6 ağ floodfill katılımı** ile sonuçlanıyor.

Elle yapılandırılmış floodfill’ler (I2P'de netDb'yi barındıran özel düğüm rolü), otomatik gönüllülere ek olarak vardır. floodfill sayısı eşik değerin altına düştüğünde, yüksek bant genişliğine sahip router’lar otomatik olarak gönüllü olur. Çok fazla floodfill bulunduğunda ise, floodfill rollerini bırakırlar.

### 5.2 Floodfill Rolleri

netDb (I2P ağ veritabanı) depolama iletilerini kabul etmek ve sorgulara yanıt vermenin ötesinde, floodfills (özel netDb düğümleri) standart router (yöneltici) işlevlerini yerine getirir. Daha yüksek bant genişlikleri genellikle daha fazla tunnel (tünel) katılımı anlamına gelir, ancak bu durum veritabanı hizmetleriyle doğrudan ilişkili değildir.

---

## 6. Kademlia Yakınlık Metriği

netDb, XOR tabanlı **Kademlia tarzı** mesafe ölçümü kullanır. RouterIdentity (router kimliği) veya Destination'ın SHA256 karması, Kademlia anahtarını oluşturur (LS2 Encrypted LeaseSets hariç; bunlar, tip baytı 3 ile körlenmiş açık anahtarın SHA256'sını kullanır).

### 6.1 Anahtar Uzayı Rotasyonu

Sybil saldırılarının maliyetlerini artırmak için, `SHA256(key)` kullanmak yerine sistem şunları kullanır:

```
SHA256(key + yyyyMMdd)
```
Burada tarih, 8 baytlık ASCII UTC tarihtir. Bu, **yönlendirme anahtarını** oluşturur ve UTC'ye göre her gün gece yarısında değişir—buna **anahtar uzayı rotasyonu** denir.

Yönlendirme anahtarları hiçbir zaman I2NP iletilerinde iletilmez; yalnızca yerel mesafe belirleme için kullanılır.

---

## 7. Ağ Veritabanının Bölümlendirilmesi

Geleneksel Kademlia DHT'leri, depolanan bilginin ilişkilendirilemezliğini korumaz. I2P, **segmentasyon (bölümlendirme)** uygulayarak client tunnels ile routers arasında ilişki kurulmasına yönelik saldırıları engeller.

### 7.1 Bölümlendirme Stratejisi

Routers şunları izler: - Kayıtların istemci tunnel'lar üzerinden mi yoksa doğrudan mı geldiği - Eğer tunnel üzerinden ise, hangi istemci tunnel/hedef - Birden fazla tunnel üzerinden gelenler izlenir - Depolama ile arama yanıtları birbirinden ayırt edilir

Java ve C++ gerçeklemelerinin her ikisi de şunları kullanır: - **"Ana" netDb** router bağlamında doğrudan aramalar/floodfill işlemleri için - **"İstemci Ağ Veritabanları"** veya **"Alt Veritabanları"** istemci bağlamlarında, istemci tunnel'larına gönderilen kayıtları yakalayan

Client netDbs yalnızca istemcinin yaşam süresi boyunca mevcuttur ve yalnızca istemci tunnel girişlerini içerir. İstemci tunnel kaynaklı girişler doğrudan varışlarla örtüşemez.

Her netDb, girdilerin depolama olarak mı (arama isteklerine yanıt verir) yoksa arama yanıtı olarak mı (yalnızca daha önce aynı destination (I2P'de hedef adres) için depolanmışsa yanıt verir) geldiğini izler. İstemciler sorgulara Main netDb girdileriyle asla yanıt vermez, yalnızca istemci ağ veritabanı girdileriyle yanıt verir.

Birleşik stratejiler, netDb'yi istemci-router ilişkilendirme saldırılarına karşı **bölümlendirir**.

---

## 8. Depolama, Doğrulama ve Sorgulama

### 8.1 RouterInfo'nun Eşlere Depolanması

NTCP veya SSU transport bağlantısı başlatılması sırasında yerel RouterInfo değişimini içeren I2NP `DatabaseStoreMessage`.

### 8.2 LeaseSet'in Eşlere Depolanması

Yerel LeaseSet içeren I2NP `DatabaseStoreMessage` iletileri, Destination (I2P adresi) trafiğiyle birlikte paketlenmiş ve garlic encryption ile şifrelenmiş iletiler üzerinden periyodik olarak değiş tokuş edilir; böylece LeaseSet sorguları olmadan yanıt verilmesine olanak tanır.

### 8.3 Floodfill Seçimi

`DatabaseStoreMessage` geçerli yönlendirme anahtarına en yakın floodfill'e gönderilir. En yakın floodfill yerel veritabanı aramasıyla bulunur. Gerçekte en yakın olmasa bile, flooding (yayma tekniği) onu birden fazla floodfill'e göndererek "daha yakın"a getirir.

Geleneksel Kademlia, ekleme işleminden önce "en yakınını bulma" aramasını kullanır. I2NP'de bu tür mesajlar bulunmasa da, router'lar gerçek en yakın eşin keşfini sağlamak için en düşük anlamlı biti tersleyerek (`key ^ 0x01`) yinelemeli arama gerçekleştirebilir.

### 8.4 RouterInfo'ların floodfill'lere (özel netDb dizin düğümleri) depolanması

Routers, RouterInfo'yu bir floodfill'e doğrudan bağlanıp, sıfırdan farklı bir Yanıt Jetonu içeren I2NP `DatabaseStoreMessage` göndererek yayınlar. Mesaj, uçtan uca garlic encryption (I2P'de çoklu iletileri tek pakette sarmalayan şifreleme tekniği) ile şifrelenmez (doğrudan bağlantı, aracı yoktur). Floodfill, Yanıt Jetonunu Mesaj Kimliği olarak kullanarak `DeliveryStatusMessage` ile yanıt verir.

Router'lar ayrıca RouterInfo'yu keşif amaçlı tunnel üzerinden de gönderebilir (bağlantı sınırları, uyumsuzluk, IP gizleme). Floodfill'ler aşırı yük sırasında bu tür depolama isteklerini reddedebilir.

### 8.5 LeaseSet'lerin Floodfill'lere Depolanması

LeaseSet depolaması (I2P destinasyonunun erişim bilgisi kaydı), RouterInfo'ya kıyasla daha hassastır. Router'lar, LeaseSet'in kendileriyle ilişkilendirilmesini engellemelidir.

Router'lar, giden istemci tunnel üzerinden, sıfır olmayan bir Reply Token (yanıt jetonu) içeren `DatabaseStoreMessage` ile LeaseSet yayınlar. İleti, Destination (hedef kimlik) nesnesinin Session Key Manager'ı (oturum anahtarı yöneticisi) kullanılarak uçtan uca garlic encryption ile şifrelenir; böylece tunnel'in giden uç noktasından gizlenir. floodfill, gelen tunnel üzerinden geri dönen `DeliveryStatusMessage` ile yanıt verir.

### 8.6 Flooding (ağda verinin komşu düğümlere iletilerek yayılması) Süreci

Floodfills (floodfill düğümleri), yük, netdb boyutu ve diğer faktörlere bağlı uyarlanabilir ölçütleri kullanarak, yerelde saklamadan önce RouterInfo/LeaseSet'i doğrular.

Geçerli ve daha yeni veriyi aldıktan sonra, floodfill'ler, yönlendirme anahtarına en yakın 3 floodfill router'ı bularak onu "flood" eder. Doğrudan bağlantılar, sıfır Reply Token (Yanıt Jetonu) ile I2NP `DatabaseStoreMessage` gönderir. Diğer router'lar yanıt vermez veya yeniden "flood" etmez.

**Önemli kısıtlamalar:** - Floodfills, tunnels üzerinden flood yapmamalıdır; yalnızca doğrudan bağlantılar - Floodfills, süresi dolmuş LeaseSet veya yayımlanmasının üzerinden bir saatten fazla geçmiş RouterInfo için asla flood yapmaz

### 8.7 RouterInfo ve LeaseSet Sorgulaması

I2NP `DatabaseLookupMessage`, floodfill router'lardan netDb girdilerini ister. Sorgular, giden keşif tunnel üzerinden gönderilir; yanıtlar, dönüş için kullanılacak gelen keşif tunnel'ini belirtir.

Sorgular genellikle, istenen anahtara en yakın iki "iyi" floodfill router'a, paralel olarak gönderilir.

- **Yerel eşleşme**: I2NP `DatabaseStoreMessage` yanıtını alır
- **Yerel eşleşme yok**: anahtara yakın diğer floodfill router (netDb'yi tutup yayımlayan özel router) referanslarıyla birlikte I2NP `DatabaseSearchReplyMessage` alır

LeaseSet sorguları, uçtan uca garlic encryption (garlic şifreleme tekniği) kullanır (0.9.5 itibarıyla). RouterInfo sorguları ise ElGamal’in hesaplama maliyeti nedeniyle şifrelenmez; bu da onları giden uç nokta dinlemesine karşı savunmasız hale getirir.

0.9.7 sürümünden itibaren, sorgu yanıtları oturum anahtarı ve etiket içerir; bu da yanıtları gelen ağ geçidinden gizler.

### 8.8 Yinelemeli Sorgular

0.8.9 öncesi: Özyinelemeli veya yinelemeli yönlendirme olmadan iki paralel yedekli sorgu.

0.8.9 itibarıyla: **Yinelemeli sorgular** yedeksiz olarak uygulandı—daha verimli, güvenilir ve eksik floodfill bilgisine daha uygundur. Ağlar büyüdükçe ve router'lar daha az floodfill bildikçe, sorgular O(log n) karmaşıklığına yaklaşır.

Yinelemeli aramalar, daha yakın eş referansları olmasa bile sürdürülür; bu da kötücül black-holing (trafiği kasıtlı olarak kara deliğe yönlendirme) girişimlerini önler. Geçerli azami sorgu sayısı ve zaman aşımı uygulanır.

### 8.9 Doğrulama

**RouterInfo Doğrulaması**: "Practical Attacks Against the I2P Network" makalesinde açıklanan saldırıları önlemek için 0.9.7.1 itibarıyla devre dışı bırakıldı.

**LeaseSet (kiralama kümesi) Doğrulaması**: Routers (yönlendiriciler) ~10 saniye bekler, ardından farklı bir floodfill (düğümü) üzerinden giden istemci tunnel (tünel) aracılığıyla sorgulama yapar. Uçtan uca garlic encryption (şifreleme tekniği) bunu giden uç noktadan gizler. Yanıtlar gelen tunnels üzerinden geri döner.

0.9.7 sürümünden itibaren, yanıtlar, oturum anahtarı/etiket gizleme kullanılarak inbound gateway (gelen ağ geçidi) karşısında gizli kalacak biçimde şifrelenir.

### 8.10 Keşif

**Keşif**, yeni router'ları keşfetmek için rastgele anahtarlarla netdb araması yapmayı içerir. Floodfills, istenen anahtara yakın non-floodfill router hash'lerini içeren `DatabaseSearchReplyMessage` ile yanıt verir. Keşif sorguları `DatabaseLookupMessage` içinde özel bir bayrak ayarlar.

---

## 9. MultiHoming (birden fazla ağ bağlantısı/sağlayıcı ile çalışma)

Özdeş özel/açık anahtarlar (geleneksel `eepPriv.dat`) kullanan Destinasyonlar, aynı anda birden fazla router üzerinde barındırılabilir. Her örnek periyodik olarak imzalı LeaseSet'ler yayımlar; en son yayımlanan LeaseSet, sorgu yapanlara döner. LeaseSet yaşam süreleri en fazla 10 dakika olduğundan, kesintiler en fazla ~10 dakika sürer.

0.9.38 itibarıyla, **Meta LeaseSets**, ortak hizmetler sunan ayrı Destinations kullanarak büyük multihomed (birden fazla bağımsız bağlantı/uç nokta barındıran) hizmetleri destekler. Meta LeaseSet girişleri, geçerlilik süreleri 18.2 saate kadar olan Destinations veya diğer Meta LeaseSets olup, ortak hizmetleri barındıran yüzlerce/binlerce Destinations’a olanak tanır.

---

## 10. Tehdit Analizi

Yaklaşık 1700 floodfill router şu anda çalışıyor. Ağın büyümesi, çoğu saldırıyı zorlaştırır veya etkisini azaltır.

### 10.1 Genel Önlemler

- **Büyüme**: Daha fazla floodfills, saldırıları daha zor hale getirir veya daha az etkili kılar
- **Yedeklilik**: Tüm netdb girdileri, anahtara en yakın 3 floodfill routers üzerinde flooding (sel tipi yayma yöntemi) yoluyla depolanır
- **İmzalar**: Tüm girdiler, oluşturucuları tarafından imzalanır; sahtecilik imkansızdır

### 10.2 Yavaş veya Yanıt Vermeyen Routers

Router'lar, floodfill'ler için genişletilmiş eş profili istatistiklerini tutar: - Ortalama yanıt süresi - Sorgu yanıtlama yüzdesi - Depolama doğrulaması başarı yüzdesi - Son başarılı depolama - Son başarılı sorgulama - Son yanıt

Router'lar, en yakın floodfill'i seçmeye yönelik "goodness" (uygunluk ölçütü) değerini belirlerken bu metrikleri kullanır. Tamamen yanıtsız router'lar hızla saptanır ve bunlardan kaçınılır; kısmen kötü niyetli router'lar ise daha büyük bir zorluk teşkil eder.

### 10.3 Sybil Saldırısı (Tam Anahtar Uzayı)

Saldırganlar, etkili bir DoS saldırısı olarak, anahtar uzayının geneline dağıtılmış çok sayıda floodfill router oluşturabilir.

"bad" ataması için yeterince uygunsuz davranmıyorsa, olası yanıtlar şunları içerir: - Konsol haberleri, web sitesi, forum aracılığıyla duyurulan "bad" router hash/IP listelerinin derlenmesi - Ağ genelinde floodfill etkinleştirmesi ("daha fazla Sybil ile Sybil'e karşı savaş") - Sabit kodlanmış "bad" listeleri içeren yeni yazılım sürümleri - Otomatik tanımlama için geliştirilmiş eş profili metrikleri ve eşik değerleri - Tek bir IP blok içinde birden fazla floodfill'i diskalifiye eden IP blok nitelendirmesi - Otomatik aboneliğe dayalı kara liste (Tor konsensüsüne benzer)

Daha büyük ağlar bunu zorlaştırır.

### 10.4 Sybil Saldırısı (Kısmi Anahtar Uzayı)

Saldırganlar, anahtar uzayında birbirine çok yakın kümelenmiş 8–15 floodfill router oluşturabilir. Bu anahtar uzayına yönelik tüm arama/kaydetme işlemleri saldırgan router'lara yönlendirilir; bu da belirli I2P sitelerinde DoS (hizmet engelleme) yapılmasını mümkün kılar.

Anahtar uzayı kriptografik SHA256 özetlerini indekslediğinden, saldırganların yeterli yakınlığa sahip routers oluşturmak için kaba kuvvete başvurması gerekir.

**Savunma**: Kademlia yakınlık algoritması, `SHA256(key + YYYYMMDD)` kullanarak zaman içinde değişir; günlük değişim UTC gece yarısında gerçekleşir. Bu **keyspace rotation** (anahtar uzayı rotasyonu), saldırının her gün yeniden oluşturulmasını zorlar.

> **Not**: Son araştırmalar, anahtar uzayı rotasyonunun pek etkili olmadığını gösteriyor—saldırganlar router hash'lerini önceden hesaplayabilir ve rotasyondan sonra yarım saat içinde anahtar uzayının bazı kısımlarını gölgede bırakmak için yalnızca birkaç router yeterlidir.

Günlük rotasyonun sonucu: dağıtılmış netdb, rotasyondan sonra birkaç dakika boyunca güvenilmez hale gelir—yeni en yakın router store iletilerini alana kadar sorgular başarısız olur.

### 10.5 Önyükleme Saldırıları

Saldırganlar reseed websites (yeni router’ların ağa ilk katılımında eş bilgilerini sağlamak için kullanılan web siteleri) ele geçirebilir veya geliştiricileri kötücül reseed websites eklemeye kandırabilir; böylece yeni router’ları izole/çoğunluk kontrolündeki ağlara önyükleyebilir.

**Uygulanan Savunmalar:** - Tek bir site yerine birden fazla reseed (ağ önyükleme) sitesinden RouterInfo (yöneltici bilgisi veri yapısı) alt kümelerinin alınması - Ağ dışı reseed izlemesiyle sitelerin periyodik olarak yoklanması - 0.9.14 itibarıyla, reseed veri paketleri imzalı zip dosyalarıdır ve indirilen imzalar doğrulanır (bkz. [su3 specification](/docs/specs/updates))

### 10.6 Sorgu Yakalama

Floodfill router'lar, döndürülen referanslar aracılığıyla eşleri saldırganın kontrolündeki router'lara "yönlendirebilir".

Düşük sıklık nedeniyle keşif yoluyla olması pek olası değil; routers, eş referanslarını esas olarak normal tunnel oluşturma yoluyla edinir.

0.8.9 itibarıyla, yinelemeli aramalar uygulanmıştır. `DatabaseSearchReplyMessage` floodfill referansları, arama anahtarına daha yakınsa izlenir. İstek yapan router'lar referans yakınlığına güvenmez. Daha yakın anahtarlar bulunmasa bile aramalar zaman aşımı/azami sorgu sayısına kadar sürer; bu da kötü niyetli black-holing (trafiği yutma saldırısı) girişimlerini önler.

### 10.7 Bilgi Sızıntıları

I2P'deki DHT (dağıtık karma tablosu) bilgi sızıntısı daha fazla araştırma gerektiriyor. floodfill router'lar, sorguları gözlemleyerek bilgi toplar. Kötücül düğüm oranı %20 seviyesindeyken, daha önce açıklanan Sybil (çoklu sahte kimlik) tehditleri birden fazla nedenle sorunlu hâle gelir.

---

## 11. Gelecek Çalışmalar

- Ek netDb sorguları ve yanıtları için uçtan uca şifreleme
- Daha iyi sorgu yanıtı izleme yöntemleri
- keyspace (anahtar uzayı) rotasyonu güvenilirlik sorunlarına yönelik azaltma yöntemleri

---

## 12. Referanslar

- [Ortak Yapılar Teknik Belirtimi](/docs/specs/common-structures/) – RouterInfo ve LeaseSet yapıları
- [I2NP Teknik Belirtimi](/docs/specs/i2np/) – Veritabanı mesaj türleri
- [Öneri 123: Yeni netDb Girdileri](/proposals/123-new-netdb-entries) – LeaseSet2 teknik belirtimi
- [Tarihsel netDb Tartışması](/docs/netdb/) – Geliştirme geçmişi ve arşivlenmiş tartışmalar
