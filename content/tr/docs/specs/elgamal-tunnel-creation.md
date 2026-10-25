---
title: "Tunnel Oluşturma Spesifikasyonu (ElGamal)"
description: "X25519 ile değiştirilen eski ElGamal tabanlı tunnel oluşturma spesifikasyonu"
slug: "elgamal-tunnel-creation"
aliases:
  - "/tr/tunnel-alt-creation"
  - "/tr/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Genel Bakış {#tunnelcreate-overview}

NOT: ESKİMİŞ - Bu ElGamal tunnel yapı spesifikasyonudur. Güncel yöntem için [X25519 tunnel yapı spesifikasyonuna](/docs/specs/tunnel-creation-ecies) bakınız.

Bu belge, "etkileşimsiz teleskoplama" yöntemi kullanarak tunnel oluşturmak için kullanılan şifreli tunnel yapı mesajlarının ayrıntılarını belirtir. Peer seçimi ve sıralama yöntemleri dahil olmak üzere sürecin genel bir görünümü için tunnel yapı belgesi [TUNNEL-IMPL](/docs/specs/tunnel-implementation) bölümüne bakın.

Tunnel oluşturma, tunnel içindeki peer'ların yolu boyunca iletilen, yerinde yeniden yazılan ve tunnel oluşturucusuna geri gönderilen tek bir mesaj ile gerçekleştirilir. Bu tek tunnel mesajı değişken sayıda kayıttan (8'e kadar) oluşur - tunnel içindeki her potansiyel peer için bir tane. Bireysel kayıtlar, yol boyunca sadece belirli bir peer tarafından okunabilmesi için asimetrik olarak (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) şifrelenir, aynı zamanda asimetrik olarak şifrelenmiş kaydı sadece uygun zamanda açığa çıkarmak için her hop'ta ek bir simetrik şifreleme katmanı (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) eklenir.

### Kayıt Sayısı {#number}

Tüm kayıtların geçerli veri içermesi gerekmez. Örneğin, 3 hop'luk bir tunnel için build mesajı, tunnel'ın gerçek uzunluğunu katılımcılardan gizlemek için daha fazla kayıt içerebilir. İki tür build mesajı vardır. Orijinal Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) 8 kayıt içerir, bu da herhangi bir pratik tunnel uzunluğu için fazlasıyla yeterlidir. Daha yeni Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) 1 ila 8 kayıt içerir. Başlatan taraf, mesaj boyutu ile istenen tunnel uzunluğu gizleme miktarı arasında bir denge kurabilir.

Mevcut ağda, çoğu tunnel 2 veya 3 hop uzunluğundadır. Mevcut uygulama, 4 hop veya daha kısa tunnel'ları oluşturmak için 5 kayıtlı VTBM kullanır ve daha uzun tunnel'lar için 8 kayıtlı TBM kullanır. 5 kayıtlı VTBM (parçalandığında üç 1KB tunnel mesajına sığar) ağ trafiğini azaltır ve oluşturma başarı oranını artırır, çünkü daha küçük mesajların düşürülme olasılığı daha azdır.

Yanıt mesajı, yapı mesajı ile aynı tür ve uzunlukta olmalıdır.

### Talep Kaydı Spesifikasyonu {#tunnelcreate-requestrecord}

Ayrıca I2NP Spesifikasyonu [BRR](/docs/specs/i2np#struct-buildrequestrecord)'de belirtilmiştir.

Kaydın düz metni, yalnızca sorguya konu olan hop tarafından görülebilir:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Sonraki tunnel ID ve sonraki router kimlik hash alanları, tunnel'daki bir sonraki atlamayı belirtmek için kullanılır, ancak giden tunnel uç noktası için, yeniden yazılan tunnel oluşturma yanıt mesajının nereye gönderilmesi gerektiğini belirtirler. Ayrıca, sonraki mesaj ID'si, mesajın (veya yanıtın) kullanması gereken mesaj ID'sini belirtir.

Tunnel katman anahtarı, tunnel IV anahtarı, yanıt anahtarı ve yanıt IV'ü, yalnızca bu yapı isteği kaydında kullanılmak üzere oluşturucu tarafından üretilen her biri rastgele 32 baytlık değerlerdir.

Flags alanı şunları içerir:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Bit 7, hop'un bir inbound gateway (IBGW) olacağını gösterir. Bit 6, hop'un bir outbound endpoint (OBEP) olacağını gösterir. Her iki bit de ayarlanmamışsa, hop bir ara katılımcı olacaktır. Her ikisi aynı anda ayarlanamaz.

#### İstek Kaydı Oluşturma

Her hop rastgele bir Tunnel ID alır, sıfır olmayan. Mevcut ve sonraki hop Tunnel ID'leri doldurulur. Her kayıt rastgele bir tunnel IV anahtarı, yanıt IV'si, katman anahtarı ve yanıt anahtarı alır.

#### İstek Kaydı Şifreleme {#encryption}

Bu açık metin kaydı, atlama noktasının genel şifreleme anahtarı ile ElGamal 2048 şifrelemesi [CRYPTO-ELG](/docs/specs/cryptography#elgamal) kullanılarak şifrelenir ve 528 baytlık bir kayda formatlanır:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
512 baytlık şifrelenmiş kayıtta, ElGamal verisi 514 baytlık ElGamal şifrelenmiş bloğun [CRYPTO-ELG](/docs/specs/cryptography#elgamal) 1-256 ve 258-513 baytlarını içerir. Bloktan gelen iki dolgu baytı (0 ve 257 konumlarındaki sıfır baytları) kaldırılır.

Cleartext tam alanı kullandığından, `SHA256(cleartext) + cleartext` dışında ek padding'e gerek yoktur.

Her 528 baytlık kayıt daha sonra yinelemeli olarak şifrelenir (AES şifre çözme kullanılarak, her hop için yanıt anahtarı ve yanıt IV'si ile) böylece router kimliği yalnızca söz konusu hop için düz metin halinde olur.

### Hop İşleme ve Şifreleme {#tunnelcreate-hopprocessing}

Bir hop bir TunnelBuildMessage aldığında, içindeki kayıtları kendi kimlik hash'i (16 bayta kısaltılmış) ile başlayanları bulmak için inceler. Daha sonra o kayıttan ElGamal bloğunu çözer ve korumalı açık metni alır. Bu noktada, AES-256 yanıt anahtarını bir Bloom filtresine besleyerek tunnel isteğinin tekrar olmadığından emin olurlar. Tekrarlar veya geçersiz istekler düşürülür. Mevcut saat veya saatin başından kısa bir süre sonraysa önceki saat ile damgalanmamış kayıtlar düşürülmelidir. Örneğin, zaman damgasındaki saati alın, tam bir zamana dönüştürün, ardından mevcut zamandan 65 dakikadan fazla geri veya 5 dakika ileriyse geçersizdir. Bloom filtresi en az bir saat süresine (artı birkaç dakika, saat sapmasına izin vermek için) sahip olmalıdır, böylece kayıttaki saat zaman damgasını kontrol ederek reddedilmeyen mevcut saatteki tekrar kayıtlar, filtre tarafından reddedilecektir.

Tunnel'a katılmayı kabul edip etmeyeceklerine karar verdikten sonra, isteği içeren kaydı şifrelenmiş bir yanıt bloğu ile değiştirirler. Diğer tüm kayıtlar, dahil edilen yanıt anahtarı ve IV ile AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) ile şifrelenir. Her biri aynı yanıt anahtarı ve yanıt IV'si ile ayrı ayrı AES/CBC ile şifrelenir. CBC modu kayıtlar arasında devam ettirilmez (zincirlenmez).

Her hop yalnızca kendi yanıtını bilir. Eğer kabul ederse, kullanılmayacak olsa bile tunnel'ı sona erme süresine kadar koruyacaktır, çünkü diğer tüm hop'ların kabul edip etmediğini bilemez.

#### Yanıt Kaydı Spesifikasyonu {#tunnelcreate-replyrecord}

Mevcut hop kendi kaydını okuduktan sonra, tunnel'a katılmayı kabul edip etmediklerini belirten bir yanıt kaydıyla değiştirir ve eğer katılmıyorlarsa, reddedilme nedenlerini sınıflandırırlar. Bu basitçe 1 bayt değerdir, 0x0 tunnel'a katılmayı kabul ettikleri anlamına gelir ve daha yüksek değerler daha yüksek reddedilme seviyelerini ifade eder.

Aşağıdaki ret kodları tanımlanmıştır:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Router kapanması gibi diğer nedenleri eşlerden gizlemek için, mevcut uygulama neredeyse tüm reddedmeler için TUNNEL_REJECT_BANDWIDTH kullanır.

Yanıt, şifrelenmiş blokta kendisine iletilen AES oturum anahtarı ile şifrelenir ve tam kayıt boyutuna ulaşmak için 495 bayt rastgele veri ile doldurulur. Dolgu, durum baytından önce yerleştirilir:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Bu aynı zamanda I2NP spesifikasyonunda [BRR](/docs/specs/i2np#struct-buildrequestrecord) da açıklanmaktadır.

### Tunnel İnşa Mesajı Hazırlığı {#tunnelcreate-requestpreparation}

Yeni bir Tunnel Build Message oluştururken, tüm Build Request Records önce oluşturulmalı ve ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal) kullanılarak asimetrik olarak şifrelenmelidir. Her kayıt daha sonra, AES [CRYPTO-AES](/docs/specs/cryptography#AES) kullanılarak yoldaki önceki hop'ların yanıt anahtarları ve IV'leri ile önceden şifresi çözülür. Bu şifre çözme işlemi ters sırada çalıştırılmalıdır, böylece asimetrik olarak şifrelenmiş veriler, önceki hop şifreledikten sonra doğru hop'ta açık olarak görünecektir.

Bireysel istekler için gerekli olmayan fazla kayıtlar, yaratıcı tarafından basitçe rastgele verilerle doldurulur.

### Tunnel İnşa Mesajı Teslimatı {#tunnelcreate-requestdelivery}

Giden tunnel'lar için, teslimat doğrudan tunnel oluşturucusundan ilk hop'a yapılır ve TunnelBuildMessage, oluşturucunun tunnel'daki başka bir hop gibi paketlenmesiyle gerçekleştirilir. Gelen tunnel'lar için ise teslimat mevcut bir giden tunnel üzerinden yapılır. Giden tunnel genellikle inşa edilen yeni tunnel ile aynı havuzdan gelir. O havuzda mevcut giden tunnel yoksa, giden keşif tunnel'ı kullanılır. Başlangıçta, henüz giden keşif tunnel'ı mevcut değilken, sahte bir 0-hop giden tunnel kullanılır.

### Tunnel Build Message Endpoint Handling {#tunnelcreate-endpointhandling}

Giden tunnel oluşturulması için, istek giden uç noktaya ulaştığında ('herkese mesaj göndermeye izin ver' bayrağı ile belirlendiği gibi), atlama normal şekilde işlenir, kaydın yerine şifrelenmiş bir yanıt oluşturulur ve diğer tüm kayıtlar şifrelenir, ancak TunnelBuildMessage'ın iletileceği 'sonraki atlama' olmadığından, bunun yerine şifrelenmiş yanıt kayıtlarını bir TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) veya VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) içine yerleştirir (mesaj türü ve kayıt sayısı isteğinkiyle eşleşmelidir) ve bunu istek kaydında belirtilen yanıt tunnel'ına teslim eder. Bu yanıt tunnel'ı, Tunnel Build Reply Message'ını tıpkı diğer mesajlarda olduğu gibi tunnel yaratıcısına geri iletir [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). Tunnel yaratıcısı daha sonra bunu aşağıda açıklandığı şekilde işler.

Yanıt tunnel'ı, oluşturucu tarafından şu şekilde seçildi: Genellikle, oluşturulan yeni giden tunnel ile aynı havuzdan gelen bir giriş tunnel'ıdır. O havuzda mevcut bir giriş tunnel'ı yoksa, bir giriş keşif tunnel'ı kullanılır. Başlangıçta, henüz hiçbir giriş keşif tunnel'ı mevcut değilken, sahte bir 0-atlama giriş tunnel'ı kullanılır.

Bir inbound tunnel oluşturulması için, istek inbound endpoint'e (tunnel creator olarak da bilinir) ulaştığında, açık bir Tunnel Build Reply Message üretmeye gerek yoktur ve router aşağıdaki gibi her yanıtı işler.

### Tunnel Oluşturma Yanıt Mesajı İşleme {#tunnelcreate-replyprocessing}

Yanıt kayıtlarını işlemek için, oluşturucu sadece her kaydı ayrı ayrı AES ile şifresini çözmek zorundadır, eş düğümden sonraki tunnel'daki her hop'un yanıt anahtarını ve IV'sini (ters sırayla) kullanarak. Bu daha sonra tunnel'a katılmayı kabul edip etmediklerini veya neden reddettiklerini belirten yanıtı ortaya çıkarır. Hepsi kabul ederse, tunnel oluşturulmuş sayılır ve hemen kullanılabilir, ancak herhangi biri reddederse, tunnel atılır.

Kabul ve reddetmeler, gelecekteki peer tunnel kapasitesi değerlendirmelerinde kullanılmak üzere her peer'ın profilinde [PEER-SELECTION](/docs/overview/peer-selection) not edilir.

## Geçmiş ve Notlar {#tunnelcreate-notes}

Bu strateji, Michael Rogers, Matthew Toseland (toad) ve jrandom arasında I2P mail listesinde predecessor saldırısı hakkında yapılan bir tartışma sırasında ortaya çıktı. Bkz. [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Bu strateji 2006-02-16 tarihinde yayınlanan 0.6.1.10 sürümünde tanıtıldı ve bu, I2P'de geriye dönük uyumluluğu olmayan bir değişikliğin yapıldığı son seferydi.

Notlar:

- Bu tasarım, bir tunnel içindeki iki düşmanca peer'ın aynı tunnel içinde olduklarını tespit etmek için bir veya daha fazla istek veya yanıt kaydını etiketlemesini engellemez, ancak bunu yapmak tunnel yaratıcısı tarafından yanıtı okurken tespit edilebilir ve tunnel'ın geçersiz olarak işaretlenmesine neden olur.

- Bu tasarım asimetrik olarak şifrelenmiş bölümde bir proof of work içermez, ancak 16 baytlık kimlik hash'i yarıya indirilebilir ve ikinci yarısı 2^64 maliyete kadar bir hashcash fonksiyonu ile değiştirilebilir.

- Bu tasarım tek başına tunnel içindeki iki düşmanca peer'ın zamanlama bilgisini kullanarak aynı tunnel'da olup olmadıklarını belirlemelerini engellemez. Toplu ve senkronize istek teslimi kullanımı yardımcı olabilir (istekleri toplayıp (ntp-senkronize) dakikada göndermek). Ancak, bunu yapmak peer'ların istekleri geciktirerek ve gecikmelerini tunnel'da daha sonra tespit ederek istekleri 'etiketlemelerine' izin verir, küçük bir pencerede teslim edilmeyen isteklerin düşürülmesi işe yarayabilir (ancak bunu yapmak yüksek derecede saat senkronizasyonu gerektirir). Alternatif olarak, belki de bireysel hop'lar isteği iletmeden önce rastgele bir gecikme ekleyebilir?

- İsteği etiketlemek için ölümcül olmayan herhangi bir yöntem var mı?

- Tekrar saldırısı (replay) önleme için bir saatlik çözünürlükte zaman damgası kullanılır. Bu kısıtlama 0.9.16 sürümüne kadar zorunlu kılınmamıştı.

## Gelecekteki Çalışmalar {#future}

- Mevcut uygulamada, başlatıcı kendisi için bir kaydı boş bırakır.
  Dolayısıyla n kayıtlı bir mesaj yalnızca n-1 hop'luk bir tunnel oluşturabilir.
  Bu, gelen tunnel'lar için gerekli gibi görünmektedir (sondan bir önceki hop'un
  bir sonraki hop için hash önekini görebildiği durumda), ancak giden tunnel'lar için gerekli değildir.
  Bu araştırılıp doğrulanması gereken bir konudur. Kalan kaydın anonimliği tehlikeye atmadan
  kullanılması mümkünse, bunu yapmalıyız.

- Yukarıdaki notlarda açıklanan olası etiketleme ve zamanlama saldırılarının daha ayrıntılı analizi.

- Yalnızca VTBM kullanın; onu desteklemeyen eski peer'ları seçmeyin.

- Build Request Record bir tunnel yaşam süresi veya son kullanma tarihi belirtmez;
  her hop tunnel'ı 10 dakika sonra sonlandırır, bu ağ genelinde
  sabitlenmiş bir sabittir. Flag alanında bir bit kullanabilir ve padding'den 4 (veya 8)
  byte çıkararak bir yaşam süresi veya son kullanma tarihi belirtebiliriz. İstekte bulunan
  bu seçeneği yalnızca tüm katılımcılar desteklediğinde belirtir.

## Referanslar {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
