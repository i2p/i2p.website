---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Not
Ağ dağıtımı ve testleri devam ediyor.
Küçük revizyonlar yapılabilir.
Resmi spesifikasyon için [SPEC](/en/docs/spec/ecies/) görebilirsiniz.

0.9.46 itibariyle uygulanmamış olan özellikler şunlardır:

- Mesaj Numaraları, Seçenekler ve Sonlandırma blokları
- Protokol katmanı yanıtları
- Sıfır statik anahtar
- Multicast


## Genel Bakış

Bu, I2P'nin başlangıcından bu yana ilk yeni uçtan-uca şifreleme türü için bir öneridir ve ElGamal/AES+Oturum Etiketleri yerine kullanılacaktır [Elg-AES](/en/docs/spec/elgamal-aes/).

Aşağıdaki gibi önceki çalışmalara dayanır:

- Ortak yapılar spesifikasyonu [Common](/en/docs/spec/common-structures/)
- LS2 dahil olmak üzere [I2NP](/en/docs/spec/i2np/) spesifikasyonu
- ElGamal/AES+Oturum Etiketler [Elg-AES](/en/docs/spec/elgamal-aes/)
- http://zzz.i2p/topics/1768 yeni asimetrik şifreleme genel bakış
- Alt seviye kripto genel bakış [CRYPTO-ELG](/en/docs/how/cryptography/)
- ECIES http://zzz.i2p/topics/2418
- [NTCP2](/en/docs/transport/ntcp2/) [Prop111](/en/proposals/111-ntcp2/)
- 123 Yeni netDB Girişleri
- 142 Yeni Kripto Şablonu
- [Noise](https://noiseprotocol.org/noise.html) protokolü
- [Signal](https://signal.org/docs/specifications/doubleratchet/) çift yönlü ratchet algoritması

Amaç, uçtan uca, hedefe-hedef iletişimini yeni şifreleme ile desteklemektir.

Tasarım, Signal'ın çift yönlü ratchet'i içeren bir Noise el sıkışması ve veri fazı kullanacaktır.

Bu öneride Signal ve Noise'a yapılan tüm referanslar yalnızca arka plan bilgisi içindir.
Bu öneriyi anlamak veya uygulamak için Signal ve Noise protokollerine ilişkin bilgi gerekmez.


### Şu Anki ElGamal Kullanımları

Bir gözden geçirme olarak,
ElGamal 256-byte'lık ortak anahtarlar aşağıdaki veri yapılarında bulunmaktadır.
Ortak yapılar spesifikasyonuna başvurun.

- Bir Yönlendirici Kimliği İçinde
  Bu, yönlendiricinin şifreleme anahtarıdır.

- Bir Hedef İçinde
  Hedefin ortak anahtarı, eski i2cp-to-i2cp şifrelemesi için kullanılıyordu
  ki bu 0.6 sürümünde devre dışı bırakıldı, şu anda kullanılmamakta,
  LeaseSet şifrelemesi için IV dışında, ki bu da ömrünü tamamlamıştır.
  Bunun yerine LeaseSet'teki ortak anahtar kullanılmaktadır.

- Bir LeaseSet İçinde
  Bu, hedefin şifreleme anahtarıdır.

- LS2 İçinde
  Bu, hedefin şifreleme anahtarıdır.



### Anahtar Sertifikalarındaki EncTypes

Bir gözden geçirme olarak,
şifreleme türlerine destek eklediğimizde imza türlerine destek ekledik.
Şifreleme türü alanı her zaman sıfırdır, hem Destinasyonlar hem de RouterKimliklerinde.
Bunun ne zaman değiştirileceği konusundaki karar verilecektir.
Ortak yapılar spesifikasyonuna [Common](/en/docs/spec/common-structures/) başvurun.




### Asimetrik Şifreleme Kullanımları

Bir gözden geçirme olarak, ElGamal'ı kullanıyoruz:

1) Tünel Oluşturma mesajları (anahtar RouterIdentity içindedir)
   Bu öneri kapsamında yer almıyor.
   152 numaralı öneriye bakın [Prop152](/en/proposals/152-ecies-tunnels/).

2) Ağ veritabanı ve diğer I2NP mesajlarının yönlendiriciye-yönlendirici şifrelemesi (Anahtar RouterIdentity içindedir)
   Bu öneriye bağlıdır.
   1) için de bir öneri gerektirir veya anahtarı RI seçeneklerine koymak gerektirir.

3) İstemci Uçtan-uca ElGamal+AES/Oturum Etiketi (anahtar LeaseSet'tedir, Hedef anahtarı kullanılmıyor)
   Bu öneri kapsamında yer almaktadır.

4) NTCP1 ve SSU için Geçici DH
   Bu öneri kapsamında yer almıyor.
   NTCP2 için 111 numaralı öneriye bakın.
   SSU2 için mevcut bir öneri bulunmamaktadır.


### Hedefler

- Geriye dönük uyumlu
- LS2 üzerine inşa eder ve gerektirir (öneri 123)
- NTCP2 için eklenen yeni kripto veya ilkel yapı taşlarından yararlanır (öneri 111)
- Destek için yeni kripto veya ilkel yapı taşları gerekmez
- Kripto ve imzalamanın ayrılığını koruyun; mevcut ve gelecekteki tüm sürümleri destekleyin
- Hedefler için yeni kripto etkinleştirin
- Yönlendiriciler için yeni kripto etkinleştirin, ancak yalnızca sarımsak mesajları için - tünel oluşturma ayrı bir öneri olacaktır
- 32 baytlık ikili hedef hash'lerine dayanan hiçbir şeyi kırmayın, örneğin bittorrent
- Geçici statik DH kullanarak 0-RTT mesaj teslimini sürdürün
- Bu protokol katmanında mesajların tamponlanmasını/kuyruklanmasını gerektirmeyin;
  bir yanıt beklemeden her iki yönde sınırsız mesaj teslimini desteklemeye devam edin
- 1 RTT'den sonra geçici-geçici DH'ye yükseltin
- Sıralama dışı mesajların işlenmesini sürdürün
- 256-bit güvenliği sürdürün
- İleriye dönük gizlilik ekleyin
- Kimlik doğrulama ekleyin (AEAD)
- ElGamal'dan çok daha fazla CPU verimli
- Java jbigi'ye DH'yi verimli hale getirme konusunda güvenmeyin
- DH işlemlerini en aza indirin
- ElGamal'dan çok daha fazla bant genişliği verimli (514 bayt ElGamal bloğu)
- İstenirse yeni ve eski kriptoyu aynı tünelde destekleyin
- Alıcı aynı tünele gelen yeni ve eski kriptoya verimli bir şekilde ayrım yapabilir
- Başkaları yeni ve eski veya gelecekteki kriptoyu ayırt edemez
- Yeni ve Mevcut Oturum uzunluğu sınıflandırmasını ortadan kaldırın (dolgu desteği)
- Yeni I2NP mesajları gerekmez
- AES yükündeki SHA-256 denetim toplamını AEAD ile değiştirin
- İletim ve alım oturumlarının protokol içinde bağlanmasını, böylece
  onaylamaların yalnızca bant dışında değil, protokolle yapılabilmesini destekleyin.
  Bu, yanıtların hemen gizlilik kazanmasına da izin verecektir.
- Şu anda CPU yükü nedeniyle yapmadığımız bazı mesajların uçtan-uca şifrelemesini etkinleştirin (RouterInfo dosyaları)
- I2NP Sarımsak Mesajı veya Sarımsak Mesajı Teslim Talimatları formatını değiştirmeyin.
- Sarımsak Clove Set ve Clove formatlarındaki kullanılmayan ve gereksiz alanları ortadan kaldırın.

Çeşitli oturum etiketi problemlerini ortadan kaldırın, bunlar arasında:

- İlk yanıt alınana kadar AES kullanılamazlığı
- Etiket teslimi varsayıldığında güvenilmezlik ve duraklamalar
- İlk teslimde çok fazla bant genişliği verimsizliği
- Etiketleri saklamak için devasa alan verimsizliği
- Etiketleri teslim etmek için devasa bant genişliği yükü
- Çok karmaşık, uygulanması zor
- Çeşitli kullanım durumları için ayarlaması zor (akış vs. datagramlar, sunucu vs. istemci, yüksek vs. düşük bant genişliği)
- Etiket teslimi nedeniyle bellek tükenmesi güvenlik açıkları


### Hedef olmayanlar / Kapsam dışı

- LS2 formatı değişiklikleri (öneri 123 tamamlandı)
- Yeni DHT rotasyon algoritması veya paylaşımlı rastgele üretim
- Tünel oluşturma için yeni şifreleme.
  152 numaralı öneriye bakın [Prop152](/en/proposals/152-ecies-tunnels/).
- Tünel katmanı şifrelemesi için yeni şifreleme.
  153 numaralı öneriye bakın [Prop153](/en/proposals/153-ecies-garlic/).
- I2NP DLM / DSM / DSRM mesajlarının şifreleme, iletim ve alım yöntemleri.
  Değişiklik yok.
- LS1 an LS2 veya ElGamal/AES'ten bu öneriye iletişim desteklenmiyor.
  Bu öneri çift yönlü bir protokoldür.
  Hedefler geriye dönük uyumluluğu, aynı tünelleri kullanarak iki leaseset yayınlayarak veya her iki şifreleme türünü de LS2'ye koyarak sağlayabilir.
- Tehdit modeli değişiklikleri
- Uygulama ayrıntıları burada tartışılmamıştır ve her projeye bırakılmıştır.
- (Olası) Çoklu aktarıma destek eklemek veya kancalar eklemek



### Gerekçelendirme

ElGamal/AES+SessionTag yaklaşık 15 yıldır şu ana kadar tek uçtan-uca protokolümüz olmuştur,
protokol için esasen herhangi bir değişiklik olmaksızın.
Şimdi daha hızlı kriptografik ilkel yapı taşlar var.
Protokolün güvenliğini artırmamız gerekiyor.
Protokolün bellek ve bant genişliği yükünü en aza indirmek için sezgisel stratejiler ve çözümler de geliştirdik, ancak bu stratejiler
hassas, ayarlaması zor ve protokolü kırılmaya daha yatkın hale getiriyor, bu da oturumun düşmesine neden oluyor.

Yaklaşık aynı zaman dilimi boyunca, ElGamal/AES+SessionTag spesifikasyonu ve ilgili belgeler
oturum etiketlerini taşımak için ne kadar bant genişliği pahalı olduğunu açıklamış,
ve oturum etiketi tesliminin yerine "senkronize edilmiş PRNG" yerleştirilmesini önermiştir.
Senkronize bir PRNG her iki uçta da aynı etiketleri deterministik olarak oluşturur,
ortak bir tohumdan türetilmiştir.
Senkronize bir PRNG, bir "ratchet" olarak da adlandırılabilir.
Bu öneri (nihayet) bu ratchet mekanizmasını belirtir ve etiket teslimatını ortadan kaldırır.

Bir ratchet (senkronize edilmiş bir PRNG) kullanarak
oturum etiketlerini üretmek, Yeni Oturum mesajında ve gerektiğinde sonraki mesajlarda
oturum etiketlerini gönderme yükünü ortadan kaldırır.
32 etiketten oluşan tipik bir etiket seti için bu 1 KB'dir.
Bu ayrıca, gönderici tarafında oturum etiketlerinin saklanmasını ortadan kaldırır,
böylece depolama gereksinimlerini yarıya indirir.

Key Compromise Impersonation (KCI) saldırılarından kaçınmak için, Noise IK desenine benzer tam bir iki yönlü el sıkışma gereklidir.
[NOISE](https://noiseprotocol.org/noise.html) içindeki Noise "Payload Security Properties" tablosuna bakın.
KCI hakkında daha fazla bilgi için makaleye bakın: https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf



### Tehdit Modeli

Tehdit modeli, NTCP2 (öneri 111) için olduğundan biraz farklı.
MitM düğümleri OBEP ve IBGW'dir ve floodfill'lerle işbirliği yaparak
güncel veya tarihsel global NetDB'yi tamamen görebildikleri varsayılır.

Amaç, bu MitM'lerin trafiği yeni ve Mevcut Oturum mesajları veya yeni kriptoya karşı eski kripto olarak sınıflandırmalarını engellemektir.



## Ayrıntılı Öneri

Bu öneri, ElGamal/AES+SessionTags'ı değiştirerek yeni bir uçtan uca protokol tanımlar.
Tasarım, Signal'ın çift yönlü ratchet'ini içeren bir Noise el sıkışması ve veri fazı kullanacaktır.


### Kriptografik Tasarımın Özeti

Protokolün yeniden tasarlanacak beş bölümü vardır:


- 1) Yeni ve Mevcut Oturum kapsayıcı formatları
  yeni formatlarla değiştirilmiştir.
- 2) ElGamal (256 bayt ortak anahtarlar, 128 bayt özel anahtarlar) yerine
  ECIES-X25519 (32 bayt ortak ve özel anahtarlar) kullanılır
- 3) AES yerine
  AEAD_ChaCha20_Poly1305 (aşağıda ChaChaPoly olarak kısaltılmış) kullanılır
- 4) Oturum Etiketleri ratchet'lerle değiştirilir,
  aslında kriptografik, senkronize bir PRNG'dir.
- 5) ElGamal/AES+SessionTags spesifikasyonunda tanımlandığı gibi AES yükü,
  NTCP2'deki format benzeri bir blok formatı ile değiştirildi.

Beş değişikliğin her biri için kendi bölümü vardır.


### I2P için Yeni Kriptografik İlkel Yapı Taşları

Mevcut I2P yönlendirici uygulamaları, mevcut I2P protokolleri için gerekmeyen
aşağıdaki standart kriptografik ilkel yapı taşları için uygulamalar gerektirecektir:

- ECIES (ama bu aslında X25519'dur)
- Elligator2

Mevcut I2P yönlendirici uygulamaları henüz [NTCP2]'yi ([Prop111](/en/proposals/111-ntcp2/)) uygulamayanlar da gerektirecektir:

- X25519 anahtar üretimi ve DH
- AEAD_ChaCha20_Poly1305 (aşağıda ChaChaPoly olarak kısaltılmıştır)
- HKDF


### Kripto Türü

LS2'de kullanılan kripto türü 4'tür.
Bu, küçük endian 32 bayt X25519 ortak anahtarını
ve burada belirtilen uçtan uca protokolü gösterir.

Kripto türü 0 ElGamal'dır.
1-3 numaralı kripto türleri ECIES-ECDH-AES-SessionTag için ayrılmıştır, 145 numaralı öneriye bakın [Prop145](/en/proposals/145-ecies/).


### Noise Protokol Çerçevesi

Bu öneri, Noise Protokol Çerçevesine [NOISE](https://noiseprotocol.org/noise.html) (Sürüm 34, 2018-07-11) dayalı gereksinimleri sağlar.
Noise, İstasyon-İstasyon protokolüne [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) benzer özelliklere sahiptir
ve bu da [SSU](/en/docs/transport/ssu/) protokolünün temelini oluşturur. Noise dilinde, Alice
başlatıcı, Bob ise yanıtlayıcıdır.

Bu öneri, Noise protokolü Noise_IK_25519_ChaChaPoly_SHA256'ye dayanır.
(Başlatma anahtar türetim fonksiyonu için
gerçek tanımlayıcı "Noise_IKelg2_25519_ChaChaPoly_SHA256"
olarak uygulanır, I2P uzantılarını belirtmek için - bkz. ADF 1 bölümü aşağıda)
Bu Noise protokolü aşağıdaki ilkel yapı taşlarını kullanır:

- Etkileşimli El Sıkışma Deseni: IK
  Alice statik anahtarını hemen Bob'a gönderir (I)
  Alice zaten Bob'un statik anahtarını biliyor (K)

- Tek Yönlü El Sıkışma Deseni: N
  Alice statik anahtarını Bob'a göndermez (N)

- DH Fonksiyonu: X25519
  X25519 DH, [RFC-7748](https://tools.ietf.org/html/rfc7748) de tanımlandığı gibi 32 bayt uzunluğunda

- Şifreleme Fonksiyonu: ChaChaPoly
  [RFC-7539](https://tools.ietf.org/html/rfc7539)'da tanımlandığı gibi AEAD_CHACHA20_POLY1305, bölüm 2.8.
  Anahtar k 32 byte, nonce n 12 byte ile
  Mesaj sırası numarası ve ilişkili verilerle (10 bayt toplam)
  NTCP2'nin tanımladığı gibi AEAD ile aynı ancak ücretsiz olup olmadığını
  kontrol edin. 16 bayt alan olan ancak ek rib'da
  şifreleme formatları.

- Hash Fonksiyonu: SHA256
  Standart 32 byte hash, I2P'de geniş ölçüde kullanılmaktadır.


Çerçevenin Eklemeleri
```````````````````````````````````

Bu öneri, Noise_IK_25519_ChaChaPoly_SHA256'ya aşağıdaki iyileştirmeleri tanımlar.  Genel olarak
[NOISE](https://noiseprotocol.org/noise.html) bölüm 13'teki yönergeleri takip ediyorlar.

1) Net geçiş rastgele anahtarları [Elligator2](https://elligator.org/) ile kodlanmıştır.

2) Yanıt açık metin etiketi ile önceden belirtilmiştir.

3) Mesaj 1 ve 2 ve veri aşaması için yük formatı tanımlanmıştır.
   Elbette, bu Noise'da tanımlıdır.

Tüm mesajlar bir [I2NP](/en/docs/spec/i2np/) Sarımsak Mesaj başlığını içerir.
Veri aşaması, Noise veri aşaması ile benzer şekilde ancak uyumsuz bir şekilde şifreleme kullanır.


### El Sıkışma Desenleri

El sıkışmalar [Noise](https://noiseprotocol.org/noise.html) el sıkışma desenlerini kullanır.

Aşağıdaki harf eşleme kullanılır:

- e = bir defalık geçici anahtar
- s = statik anahtar
- p = mesaj yükü

Tek seferlik ve Bağlı olmayan oturumlar Noise N desenine benzer.

```dataspec

<- s
  ...
  e es p ->


```

Bağlı oturumlar Noise IK desenine benzer.

```dataspec

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->


```


### Oturumlar

Mevcut ElGamal/AES+Oturum Etiketi protokolü tek yönlüdür.
Bu katmanda, alıcı bir mesajın nereden geldiğini bilmiyor.
Giden ve gelen oturumlar ilişkili değil.
Açık havadan taşınan bir DeliveryStatusMessage
(sarımsak mesajı içinde sarılmış) kullanılarak onaylamalar yapılır.

Tek yönlü bir protokolde önemli bir verimsizlik vardır.
Herhangi bir yanıt da pahalı bir 'Yeni Oturum' mesajı kullanmalıdır.
Bu daha yüksek bant genişliği, CPU ve bellek kullanımına neden olur.

Tek yönlü bir protokolde de güvenlik zaafları vardır.
Tüm oturumlar geçici-statik DH'ye dayanır.
Bir geri dönüş yolu olmadan, Bob'un statik anahtarını
geçici bir anahtara "ratchet" etmesinin bir yolu yoktur.
Bir mesajın nereden geldiğini bilmenin bir yolu olmadığında, gönderilen
geçici anahtarların giden mesajlar için
kullanılması mümkün olmaz, bu nedenle başlangıç yanıtı
da geçici-statik DH kullanır.

Bu öneri için, çift yönlü bir protokol oluşturmak için iki mekanizma
tanımlarız:
"eşleştirme" ve "bağlama".
Bu mekanizmalar verimliliği ve güvenliği artırır.


Oturum Bağlamı
````````````````````````````

ElGamal/AES+SessionTags ile olduğu gibi, tüm gelen ve giden oturumlar
belli bir bağlam içinde olmalıdır, bu ya yönlendiricinin bağlamı ya da
belirli bir yerel hedef için olan bağlamdır.
Java I2P'de, bu bağlama Oturum Anahtarı Yöneticisi denir.

Oturumlar, bağlamlar arasında paylaşılmamalıdır, çünkü bu, çeşitli yerel hedefler
arasında ya da yerel bir hedef ile bir yönlendirici arasında bir ilişki
kurulmasına izin verir.

Belirli bir hedef hem ElGamal/AES+SessionTags'ı
hem de bu öneriyi desteklediğinde, her iki oturum türü de bir bağlamı paylaşabilir.
1c) bölümüne bakın.



Gelen ve Giden Oturumların Eşleştirilmesi
```````````````````````````````````````````

Bir giden oturum orijinatörde (Alice) oluşturulduğunda,
bir giden oturumla eşleşmiş yeni bir gelen oturum oluşturulur,
eğer herhangi bir yanıt beklenmiyorsa (örneğin, ham datagramlar).

Bir yeni gelen oturum daima bir yeni giden oturumla eşleşir,
eğer herhangi bir yanıt istenmiyorsa (örneğin, ham datagramlar).

Bir yanıt istenirse ve uzak bir hedefe veya yönlendiriciye bağlıysa,
o yeni giden oturum o hedefe veya yönlendiriciye bağlanır,
ve o hedefe veya yönlendiriciye önceki herhangi bir giden oturum yerine geçer.

Gelen ve giden oturumların eşleştirilmesi, ratcheting DH anahtarlarının
yapılmasını sağlayan bir çift yönlü protokolle sonuçlanır.



Oturumları ve Hedefleri Bağlama
``````````````````````````````````

Belirli bir hedefe veya yönlendiriciye yalnızca bir giden oturum vardır.
Belirli bir hedef veya yönlendiriciden gelen birden fazla alım oturumu olabilir.
Genellikle, yeni bir gelen oturum oluşturulduğunda ve o oturumda trafik alındığında
(bu ACK olarak iş görür), diğerleri, yaklaşık bir dakika içinde sona erecek
şekilde işaretlenir.
Önceki mesajlar gönderildi (PN) değeri kontrol edilir ve önceki
gelen oturumda alınmamış bir mesaj yoksa, o
önceki oturum hemen silinebilir.

Bir giden oturum orijinatörde (Alice) oluşturulduğunda,
o, son Hedef (Bob) ile bağlanır,
ve herhangi bir eşleşmiş gelen oturum da son Hedefe bağlanır.
Oturumlar ratchet edildikçe, hedefe bağlı olarak kalırlar.

Bir gelen oturum alıcıda (Bob) oluşturulduğunda,
uzak Hedef (Alice)'e bağlanabilir, Alice'in tercihi.
Alice, Yeni Oturum mesajında bağlama bilgilerini (statik anahtarını) dahil ederse,
oturum o hedefe bağlanır,
ve bir giden oturum oluşturulur ve aynı Hedefe bağlanır.
Oturumlar ratchet edildikçe, hedefe bağlı olarak kalırlar.


Bağlama ve Eşleştirme Yararları
````````````````````````````````

Yaygın, akış durumunda, Alice ve Bob'un protokolü aşağıdaki gibi kullanmasını bekliyoruz:

- Alice yeni giden oturumunu yeni bir gelen oturumla eşleştirir, ikisi de uzak (Bob) hedefe bağlı olarak.
- Alice Yeni Oturum mesajında bağlama bilgilerini ve imzayı içerir
  Bob'a gönderir.
- Bob yeni gelen oturumunu yeni bir giden oturumla eşleştirir, ikisi de uzak (Alice) hedefe bağlı olarak.
- Bob Alice'e bir yanıt (onay) gönderir eşleşmiş oturumda, yeni bir DH anahtarına ratchet ile.
- Alice Bob'un yanıtını ve ratchet'ini aldıktan sonra, tüm sonraki mesajlar Alice'den Bob'a
ephemeral-ephemeral DH kullanır.


Mesaj Onayları
``````````````````

ElGamal/AES+SessionTags'da, bir LeaseSet bir sarımsak dişinde birleştirildiğinde,
veya etiketler teslim edildiğinde, gönderici yönlendirici bir onay talep eder.
Bu, Sarımsak Mesajında paketlenmiş bir Suplama Durum Mesajı içeren ayrı bir sarımsak dişidir.
Ek güvenlik için, Teslimat Durum Mesajı bir Sarımsak Mesajına sarılır.
Bu mekanizma, protokol perspektifinden açık havadadır.

Yeni protokolde, gelen ve giden oturumlar eşleştiği için
onaylar açık havada yapılabilir. Ayrı bir diş gerekli değildir.

Açık açık bir onay, I2NP bloğu olmayan bir Mevcut Oturum mesajıdır.
Ancak, çoğu durumda, bir açık açık onaydan kaçınılabilir, çünkü
ters trafik vardır.
Uygulamalar, akış katmanına veya uygulama katmanına yanıt
vermesi için kısa bir süre (muhtemelen yüz milisaniye)
beklemek isteyebilirler.

Uygulamalar, herhangi bir onayı göndermeden önce
I2NP bloğunun işlendiğinden emin olmalıdır,
çünkü Sarımsak Mesajı, lease set ile bir Veritabanı Deposu Mesajı içerebilir.
Geri dönüş yolunu etkili bir şekilde oluşturmak için
kısa süre önce alınmış bir lease set gerekli olacaktır,
ve geri dönüş hedefi (lease set içinde) bağlama statik
anahtarını doğrulamak için gereklidir.


Oturum Zaman Aşımı
``````````````````

Giden oturumlar her zaman gelen oturumlar önce zaman aşımına uğramalıdır.
Bir giden oturum zaman aşımına uğradığında, ve yeni biri oluşturulduğunda, yeni eşleşmiş
gelen oturum da oluşturulacaktır. Eğer eski bir gelen oturum varsa, onun
hemen sönmesine izin verilecektir.


### Multicast

TBD


### Tanımlar
Kullanılan kriptografik yapı taşlarını karşılayan işlevleri tanımlarız.

ZEROLEN
    sıfır uzunluklu bayt dizisi

CSRNG(n)
    kriptografik olarak güvenli bir rastgele sayı üretecinden n byte çıktı.

H(p, d)
    SHA-256 hash fonksiyonu, bir kişiselleştirme dizgesi p ve veri d alır,
    ve 32 byte uzunluğunda bir çıktı üretir.
    [NOISE](https://noiseprotocol.org/noise.html) 'de tanımlandığı gibi. 
    || aşağıda ekle anlamına gelir.

    SHA-256'yı aşağıdaki gibi kullanın::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    Önceki hash h ve yeni veri d'yi alarak
    32 byte uzunluğunda bir çıktı üreten SHA-256 hash fonksiyonu.
    || aşağıda ekle anlamına gelir.

    SHA-256'yı aşağıdaki gibi kullanın::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    [RFC-7539](https://tools.ietf.org/html/rfc7539)'da tanımlandığı gibi ChaCha20/Poly1305 AEAD.
    S_KEY_LEN = 32 ve S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Metni şifreleme anahtarı k ve k için benzersiz 
        n nesine kullanarak şifreler. 
        İlgili veri ad isteğe bağlıdır.
        Anahtar için düz metin boyutu 
        + HMAC için 16 baytlık bir şifreli metin döndürür.

        Anahtar gizli ise, tüm şifreli metin rastgele 
        ile ayırt edilemez olmalıdır.

    DECRYPT(k, n, ciphertext, ad)
        Şifreli metni şifreleme anahtarı k ve n olmuştur. 
        Kullanarak deşifre eder.
        İlgili veri ad isteğe bağlıdır.
        Düz metni döndürür.

DH
    X25519 ortak anahtar anlaşma sistemi. Özel anahtarlar 32 bayt, 
    ortak anahtarlar 32 bayttır, 32 bayt uzunluğunda 
    çıktılar üretirler. Aşağıdaki
    işlevlere sahiptir:

    GENERATE_PRIVATE()
        Yeni bir özel anahtar üretir.

    DERIVE_PUBLIC(privkey)
        Verilen özel anahtara karşılık gelen ortak 
        anahtarı döndürür.

    GENERATE_PRIVATE_ELG2()
        Elligator2 kodlaması için uygun bir ortak 
        anahtara eşlik eden yeni bir özel anahtar üretir.
        Not: Rastgele üretilen özel anahtarların yarısı 
        uygun olmayacak ve atılmalıdır.

    ENCODE_ELG2(pubkey)
        Verilen ortak anahtara karşılık gelen 
        Elligator2 kodlu ortak anahtarı döndürür 
        (ters eşleme).
        Kodlu anahtarlar küçük endian'dır.
        Kodlu anahtar, rasgele verilerden ayırt edilemez
        olmalı, 256 biti kaplar.
        Kodlama ve kod çözme için Elligator2 bölümüne 
        bakın.

    DECODE_ELG2(pubkey)
        Verilen Elligator2 kodlanmış ortak anahtara 
        karşılık gelen ortak anahtarı döndürür.
        Kodlama ve kod çözme için Elligator2 bölümüne bakın.

    DH(privkey, pubkey)
        Verilen özel ve ortak anahtarlardan bir paylaşılan 
        sır üretir.

HKDF(salt, ikm, info, n)
    Bazı giriş anahtarı materyalini (iyi entropiye sahip olması 
    gereken ancak uniform bir rastgele dize olması 
    gerekmeyen) ikm, 32 bayt uzunluğunda bir tuz ve 
    bağlama özel bir 'info' değeri alır 
    ve anahtar materyali olarak kullanılmaya uygun bir 
    n baytlık çıktı üretir.

    HKDF 'yi [RFC-5869](https://tools.ietf.org/html/rfc5869) 'da tanımlandığı gibi kullanın, HMAC hash 
    fonksiyonu SHA-256 gibi kullanın [RFC-2104](https://tools.ietf.org/html/rfc2104)'da tanımlandığı gibi. 
    Bu demektir ki SALT_LEN maksimum 32 bayttır.

MixKey(d)
    Önceki zincirKey ve yeni veri d ile birlikte kullanılır, 
    ve yeni chainKey ve k a ayarlar. 
    [NOISE](https://noiseprotocol.org/noise.html) 'de tanımlandığı gibi.

    HKDF 'yi aşağıdaki gibi kullanın::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Mesaj formatı


Aydı MSözde Mevcut Mesaj Biçimi
````````````````````````````````

[I2NP](/en/docs/spec/i2np/) 'de belirtildiği gibi Sarımsak Mesajı şu şekildedir.
Orta aşamalarda yeni ve eski kriptoyu ayırt edemeyecek 
şekilde bir tasarım amacı olarak bu format değiştirilemez, 
geri kalan kısmı dahil ki uzunluk alanı gereksizdir.
Format 16 baytlık tam başlıkla gösterilir, ancak
gerçek başlık kullanılan taşımaya bağlı olarak farklı bir 
format içinde olabilir.

Şifreli veriler ortaya çıkarıldığında, bir dizi Sarımsak 
Karışıkları ve ek veriler, başka bir deyişle 
Karışık Seti bulunur.

[I2NP](/en/docs/spec/i2np/) daha fazla ayrıntı ve tam bir spesifikasyon hakkında 
bilgi verir.


```dataspec

+----+----+----+----+----+----+----+----+
  |tip|      msg_id       |  son kullanma tarihi
  +----+----+----+----+----+----+----+----+
                           |  boyut   |chks|
  +----+----+----+----+----+----+----+----+
  |      uzunluk       |                   |
  +----+----+----+----+                   +
  |          Şifreli veriler               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+


```


Şifreli Veri Biçiminin Gözden Geçirilmesi
``````````````````````````````````````````

Mevcut mesaj formatı, 15 yılı aşkın süredir kullanılan
ElGamal/AES+Oturum Etiketlerdir.
ElGamal/AES+Oturum Etiketleri'nde iki mesaj formatı vardır:

1) Yeni oturum:
- 514 bayt ElGamal bloğu
- AES bloğu (128 bayt minimum, 16'nın katı)

2) Mevcut oturum:
- 32 bayt Oturum Etiketi
- AES bloğu (128 bayt minimum, 16'nın katı)

128'e dolgu, Java I2P'de uygulanmıştır ancak alımda zorunlu değildir.

Bu mesajlar I2NP sarımsak mesajında kapsüllenir; bu 
uzunluk alanı içerir, bu yüzden uzunluk 
bilinir.

Verilen, 16'ya eşit olmayan bir uzunluğa dolgu 
tanımlanmamıştır,
bu yüzden Yeni Oturum her zaman (16'ya mod 2 eşittir),
ve bir Mevcut Oturum her zaman (16'ya mod 0 eşittir).
Bunu düzeltmemiz gerekiyor.

Alıcı ilk 32 baytı bir Oturum Etiketi olarak 
aramaya çalışır.
Eğer bulunursa, AES bloğunu çözer.
Eğer bulunmazsa ve veri en az (514+16) 
uzunluğundaysa, ElGamal bloğunu çözmeye çalışır,
eğer başarılı olursa, AES bloğunu çözer.


Yeni Oturum Etiketleri ve Signal ile Karşılaştırma
``````````````````````````````````````````````````

Signal Çift Yönlü Ratchet'te, başlık şu öğeleri içerir:

- DH: Mevcut ratchet ortak anahtarı
- PN: Önceki zincir mesaj uzunluğu
- N: Mesaj Numarası

Signal'in "gönderme zincirleri" bizim etiket setlerimize 
kabaca eşdeğerdir.
Bir oturum etiketi kullanarak çoğunu ortadan kaldırabiliriz.

Yeni Oturumda, yalnızca ortak anahtarı şifrelenmemiş başlığa 
koyuyoruz.

Mevcut Oturumda, oturum etiketi başlığa eklenir.
Mevcut ratchet ortak anahtarı ile ilişkili olan
oturum etiketi ve mesaj numarası kullanılır.

Hem yeni hem de Mevcut Oturumda, PN ve N şifreli 
gövdededir.

Signal'de, her şey sürekli ratchet'lanıyor. Yeni bir DH 
ortak anahtarı, alıcının ratchet'ı
alıcı anahtarı ratchet ve yeni bir kamu anahtarı arayarak
göndermesini gerektirir.
Bu bizim için çok fazla DH işlemi olurdu.
Bu yüzden alınan anahtar onayını ve yeni bir ortak 
anın gönderilmesini ayırıyoruz.
Oturum etiketini kullanarak oturumdan gönderilen 
herhangi bir mesaj, ACK olarak işlev görür.
Yeniden anahtarları yenilemek istediğimizde 
ancak yeni bir ortak anahtar gönderiyoruz.

DH ratchet'ının gereken maksimum mesaj sayısı 65535'tir.

Bir oturum anahtarı teslim ettiğimizde, onu "Etiket Seti"nden 
türetiriz,
ayrıca oturum etiketlerini de teslim etmek zorunda kalmadan.
Bir Etiket Seti, en fazla 65536 etiket olabilir.
Ancak, alıcılar bir "ileriye dönük bakış" stratejisi uygulamalıdır,
hemen alınan son etiketin ötesinde N etiketi oluşturmak yerine.
N genellikle en fazla 128 olabilir, ancak 32 veya daha azı 
daha iyi bir seçim olabilir.



### 1a) Yeni oturum formatı

Yeni Oturum Tek Seferlik Ortak Anahtarı (32 bayt)
Şifreli veriler ve MAC (geri kalan baytlar)

Yeni Oturum mesajı göndericinin statik ortak anahtarını içerebilir veya içermeyebilir.
Eğer dahil edilirse, ters oturum o anahtarla bağlanır.
Statik anahtar dahil edilmeli, yanıtlar beklenirse,
özellikle akış ve yanıt alan veriagramlar için.
Ham veriagramlar için dahil edilmemelidir.

Yeni Oturum mesajı Noise [NOISE](https://noiseprotocol.org/noise.html) desen (desen) "N" ye (statik anahtar gönderilmezse),
veya iki yönlü desen "IK" (statik anahtar gönderilirse) benzer.



### 1b) Yeni oturum formatı (bağlama ile)

Uzunluk 96 + yük uzunluğudur.
Şifreli format:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Yeni Oturum Geçici Ortak Anahtar    |
  +             32 bayt                  +
  |     Elligator2 ile şifrelenmiş       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Statik Anahtar                +
  |       ChaCha20 şifreli veri           |
  +            32 bayt                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +    Static Key Bölümü için MAC        +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                  |
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) Yük Bölümü için            +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Ortak Anahtar :: 32 bayt, küçük endian, Elligator2, açık metin

  Statik Anahtar şifreli veriler :: 32 bayt

  Yük Bölümü şifreli verileri :: kalan veriler eksi 16 bayt

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt


```


Yeni Oturum Geçici Anahtar
``````````````````````````

Geçici anahtar 32 bayt, Elligator2 ile şifrelenmiş,
bu anahtar asla yeniden kullanılmaz;
her mesaj ile, yeniden gönderimler de dahil olmak üzere,
yeni bir anahtar oluşturulur.

Statik Anahtar
````````````

Şifrelendikten sonra, Alice'nin X25519 statik anahtarı, 32 bayt.


Yük
```````

Şifrelenmiş uzunluk verilerin kalanıdır.
Açılmış uzunluk, şifrelenmiş uzunluktan 16 daha azdır.
Yük Yanıt Süresi bloğunu içermelidir ve genellikle bir veya daha fazla Sarımsak 
Karışık bloğu içerecektir.
Format ve ek gereksinimler için yük bölümüne bakın.



### 1c) Yeni oturum formatı (bağlama olmadan)

Hiçbir yanıt gerekli değilse, hiçbir statik anahtar gönderilmez.


Uzunluk 96 + yük uzunluğudur.
Şifreli format:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Yeni Oturum Geçici Ortak Anahtar    |
  +             32 bayt                  +
  |     Elligator2 ile şifrelenmiş       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Bayraklar Bölümü            +
  |       ChaCha20 şifreli veri           |
  +            32 bayt                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) üst bölüm için             +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                  |
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) Yük Bölümü için            +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Ortak Anahtar :: 32 bayt, küçük endian, Elligator2, açık metin

  Bayraklar Bölümü şifreli veriler :: 32 bayt

  Yük Bölümü şifreli veriler :: kalan veriler eksi 16 bayt

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt


```

Yeni Oturum Geçici Anahtar
``````````````````````````

Alice'nin geçici anahtarı.
Geçici anahtar 32 bayt, Elligator2 ile kodlanmış, küçük endian.
Bu anahtar asla yeniden kullanılmaz; her mesaj ile,
tekrar gönderimler de dahil olmak üzere yeni bir anahtar oluşturulur.


Bayraklar Bölümü Şifrelenmiş Veriler
````````````````````````````````````

Bayraklar bölümü hiçbir şey içermez.
Her zaman 32 bayttır, çünkü
bağlamayla Yeni Oturum mesajları için
statik anahtarın uzunluğu ile aynı
olmalıdır.
Bob, statik anahtar mı veya bayraklar bölümü mü olduğunu
tespit etmek için 32 baytın tamamı sıfır olup olmadığını
test eder.

TODO burada gerekli herhangi bir bayrak var mı?

Yük
```````

Şifreli uzunluk verilerin kalanıdır.
Açılmış uzunluk, şifrelenmiş uzunluktan 16 daha azdır.
Yük Yanıt Süresi bloğunu içermelidir ve genellikle bir veya daha fazla Sarımsak 
Karışık bloğu içerecektir.
Format ve ek gereksinimler için yük bölümüne bakın.




### 1d) Tek seferlik format (bağlama veya oturum yok)

Sadece bir mesaj gönderilmesi bekleniyorsa,
hiçbir oturum kurulumu veya statik anahtar gerekmez.


Uzunluk 96 + yük uzunluğudur.
Şifreli format:

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Geçici Ortak Anahtar            |
  +             32 bayt                  +
  |     Elligator2 ile şifrelenmiş       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Bayraklar Bölümü            +
  |       ChaCha20 şifreli veri           |
  +            32 bayt                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) üst bölüm için             +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                  |
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) Yük Bölümü için            +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Ortak Anahtar :: 32 bayt, küçük endian, Elligator2, açık metin

  Bayraklar Bölümü şifreli veriler :: 32 bayt

  Yük Bölümü şifreli veriler :: kalan veriler eksi 16 bayt

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt


```


Yeni Oturum Bir Kez Anahtar
``````````````````````````

Bir defalık anahtar 32 bayt, Elligator2 ile kodlanmış, küçük endian.
Bu anahtar asla yeniden kullanılmaz; her mesaj ile,
tekrar gönderimler de dahil olmak üzere yeni bir anahtar oluşturulur.


Bayraklar Bölümü Şifrelenmiş Veriler
````````````````````````````````````````

Bayraklar bölümü hiçbir şey içermez.
Her zaman 32 bayttır, çünkü
bağlamayla Yeni Oturum mesajları için
statik anahtarın uzunluğu ile aynı
olmalıdır.
Bob, statik anahtar mı veya bayraklar bölümü mü olduğunu
tespit etmek için 32 baytın tamamı sıfır olup olmadığını
test eder.

TODO burada gerekli herhangi bir bayrak var mı?

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             Tamamı sıfır             +
  |              32 bayt                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  sıfırlar:: Tamamı sıfır, 32 bayt.


```


Yük
```````

Şifreli uzunluk verilerin kalanıdır.
Açılmış uzunluk, şifrelenmiş uzunluktan 16 daha azdır.
Yük Yanıt Süresi bloğunu içermelidir ve genellikle bir veya daha fazla Sarımsak 
Karışık bloğu içerecektir.
Format ve ek gereksinimler için yük bölümüne bakın.



### 1f) Yeni Oturum Mesajı için KDF'ler

Başlangıç Zincir Anahtarı için KDF
````````````````````````````````

Bu, IK için standart [NOISE](https://noiseprotocol.org/noise.html) 'dir, 
modifiye edilmiş bir protokol adı ile.
İlk oturumların (bağlı oturumlar)
ve N desenleri (bağlanmamış oturumlar) için
aynı başlatıcıyı kullanırız.

Protokol adı iki nedenden dolayı değiştirilmiştir.
İlk olarak, geçici anahtarların Elligator2
ile kodlandığını
belirtmek için ve ikinci olarak,
etiket değerinin karıştırılması için MixHash()'in çağrıldığını
belirtmek için.

```text

Bu "e" mesaj desenidir:

  // Protokol_ad tanımını yapın.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bayt, US-ASCII kodlu, NULL sonu olmayan).

  // Hash h = 32 bayt tanımlayın
  h = SHA256(protocol_name);

  32 bayt zincir anahtarı tanımlayın. h verilerini ck'ye kopyalayın.
  Zincir anahtarı ayarını yapılandırın = h

  // MixHash(null prolog)
  h = SHA256(h);

  // buraya kadar, Alice tüm giden bağlantılar için önceden hesaplayabilir


```


Bayraklar/Statik Anahtar Bölümü Şifreli İçerik için KDF
````````````````````````````````````````````````````

```text

Bu "e" mesaj desenidir:

  // Bob'un X25519 statik anahtarları
  // bpk, leaseset'te yayınlanır
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob statik ortak anahtarı
  // MixHash(bpk)
  // || aşağıda ekle anlamına gelir
  h = SHA256(h || bpk);

  // bu noktaya kadar, Bob tüm gelen bağlantılar için önceden hesaplayabilir

  // Alice'nin X25519 geçici anahtarları
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice geçici ortak anahtarı
  // MixHash(aepk)
  // || aşağıda ekle anlamına gelir
  h = SHA256(h || aepk);

  // h, Yeni Oturum Mesajında AEAD için ilgili veri olarak kullanılır
  // Elg2_aepk Yeni Oturum mesajının başında açık metin olarak gönderilir
  elg2_aepk = ENCODE_ELG2(aepk)
  // Bob tarafından tersiylenmiş
  aepk = DECODE_ELG2(elg2_aepk)

  "e" mesaj deseninin sonu.

  Bu "es" mesaj deseni:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[zincirAnahtarı, k] = MixKey(sharedSecret)
  // Şifreleme / deşifreleme için ChaChaPoly parametreleri
  anahtarVerisi = HKDF(zincirAnahtarı, paylaşılanGizli, "", 64)
  zincirAnahtarı = anahtarVerisi[0:31]

  // AEAD parametreleri
  k = anahtarVerisi[32:63]
  n = 0
  ad = h
  şifrelenmişMetin = ENCRYPT(k, n, bayraklar/statik anahtar bölümü, ad)

  "es" mesaj deseninin sonu.

  Bu "s" mesaj deseni:

  // MixHash(şifrelenmiş metin)
  // Yukarıdaki Payload bölümü KDF için kaydedin
  h = SHA256(h || şifrelenmiş metin)

  // Alice'nin X25519 statik anahtarları
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  "s" mesaj deseninin.


```



Statik Anahtarlı Yük Bölümü için KDF
``````````````````````````````````````````

```text

Bu "ss" mesaj deseni:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[zincirAnahtarı, k] = MixKey(sharedSecret)
  // Şifreleme / deşifreleme için ChaChaPoly parametreleri
  // Statik Anahtar Bölümünden zincir anahtarı
  Set paylaşılanGizli = X25519 DH sonucu
  anahtarVerisi = HKDF(zincirAnahtarı, paylaşılanGizli, "", 64)
  zincirAnahtarı = anahtarVerisi[0:31]

  // AEAD parametreleri
  k = anahtarVerisi[32:63]
  n = 0
  ad = h
  şifrelenmişMetin = ENCRYPT(k, n, yük, ad)

  "ss" mesaj deseninin sonu.

  // MixHash(şifrelenmişMetin)
  // Yeni Oturum Yanıtı KDF için kaydedin
  h = SHA256(h || şifrelenmişMetin)


```


Statik Anahtarsız Yük Bölümü için KDF
``````````````````````````````````````````

Bu bir "Noise "N" deseni, ancak bağlı oturumlar
için "IK" başlatıcıyı da kullanırız.

Yeni Oturum mesajları Alices's statik 
bu anahtar içermeyen veya içermeyen olarak 
tanımlanamaz, dokunulmaz ve onu
değiştirildiği görülene kadar şifrelenmiştir
ve statik anahtar olarak ele alındığı için
Bayraklar/Statik anahtar bölümünden ad çıkarılacaktır.

```text

zincirAnahtarı = Bayraklar/Statik anahtar bölümünden
  k = Bayraklar/Statik anahtar bölümünden
  n = 1
  ad = Bayraklar/Statik anahtar bölümünden h
  şifrelenmişMetin = ENCRYPT(k, n, yük, ad)


```



### 1g) Yeni Oturum Yanıt formatı

Tek bir Yeni Oturum mesajına karşılık olarak bir veya daha
fazla Yeni Oturum Yanıtı gönderilebilir.
Her yanıt belirli bir oturum için bir TagSet'den oluşturulan
bir etiketle öneklenir.

Yeni Oturum Yanıtı iki bölümdendir.
İlk bölüm etiket ile öne katılmış bir
Noise IK el sıkışmasının tamamlanmasıdır.
İlk bölümün uzunluğu 56 bayttır.
İkinci bölüm, veri fazı yüküdür.
İkinci bölümün uzunluğu 16 + yük uzunluğundadır.

Toplam uzunluk 72 + yük uzunluğudur.
Şifreli format:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Oturum Etiketi 8 bayt          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Geçici Ortak Anahtar           +
  |                                       |
  +            32 bayt                   +
  |     Elligator2 ile şifrelenmiş       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +  (MAC) Anahtar Bölümü için (veri yok) +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                  +
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +      (MAC) Yük Bölümü için            +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Etiket :: 8 bayt, açık metin

  Ortak Anahtar :: 32 bayt, little endian, Elligator2, açık metin

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt
         Not: ChaCha20 düz metin verileri boş (ZEROLEN)

  Yük Bölümü şifreli veriler :: kalan veriler eksi 16 bayt

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt


```

Oturum Etiketi
```````````
Etiket, altındaki DH Başlatma KDF'si
sonucunda oluşturulan TagSet'ten türetilir.
Yanıtı oturumla ilişkilendirir.
DH Başlatımı oturum 
anahtarı kullanılmaz.


Yeni Oturum Yanıtı Geçici Anahtarı
``````````````````````````````````

Bob'un geçici anahtarı.
Geçici anahtar, Elligator2 ile şifrelenmiş, 
küçük endian, 32 bayttır.
Bu anahtar asla yeniden kullanılmaz; her mesaj ile,
tekrar gönderimler de dahil olmak üzere yeni bir anahtar oluşturulur.


Yük
```````
Şifreli uzunluk, verilerin kalanıdır.
Açılmış uzunluk, şifreli kuruluş ayrı boyundan 16 daha azdır.
Yük genellikle bir veya daha fazla Sarı Kaçıklı Blok içerir.
Format ve ek gereksinimler için yük bölümüne bakın.


Yanıt TagSet KDF
`````````````````````

TagSet'den bir veya daha fazla etiket oluşturulur ve TagSet'den
yeni bir TagSet için KDF kullanılarak,
aşağıdaki ilk zincir anahtarı ile başlangıç ​​olarak,
DH Başlatma işlemi belirtilmiştir.

```text

// tagset oluştur
  tagsetKey = HKDF(zincirAnahtarı, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(zincirAnahtarı, tagsetKey)


```


Yanıt Anahtar Bölümü Şifreli İçerikler için KDF
````````````````````````````````````````````

```text

// Anahtarlar Yeni Oturum mesajından
  // Alice'in X25519 anahtarları
  // apk ve aepk orijinal Yeni Oturum mesajında gönderilir
  // ask = Alice özel statik anahtarı
  // apk = Alice ortak statik anahtarı
  // aesk = Alice özel geçici anahtarı
  // aepk = Alice geçici ortak anahtarı
  // Bob'un X25519 statik anahtarları
  // bsk = Bob özel statik anahtarı
  // bpk = Bob ortak statik anahtarı

  // Etiketi üret
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  etiket = tagsetEntry.SESSION_TAG

  // MixHash(etiket)
  h = SHA256(h || etiket)

  Bu "e" mesaj desenidir:

  // Bob'un X25519 geçici anahtarları
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob'un geçici ortak anahtarı
  // MixHash(bepk)
  // || aşağıda ekle anlamına gelir
  h = SHA256(h || bepk);

  // elg2_bepk, Yeni Oturum mesajının başında açık metin olarak gönderilir
  elg2_bepk = ENCODE_ELG2(bepk)
  // Bob tarafından kod çözülür
  bepk = DECODE_ELG2(elg2_bepk)

  "e" mesaj deseninin sonu.

  Bu "ee" mesaj desenidir:

  // MixKey(DH())
  //[zincirAnahtarı, k] = MixKey(sharedSecret)
  // Şifreleme/deşifreleme için ChaChaPoly parametreleri
  // Yeni Oturum Payload Bölümünden zincir anahtarı
  paylaşılanGizli = DH(aesk, bepk) = DH(besk, aepk)
  anahtarVerisi = HKDF(zincirAnahtarı, paylaşılanGizli, "", 32)
  zincirAnahtarı = anahtarVerisi[0:31]

  "ee" mesaj deseninin sonu.

  Bu "se" mesaj desenidir:

  // MixKey(DH())
  //[zincirAnahtarı, k] = MixKey(sharedSecret)
  paylaşılanGizli = DH(ask, bepk) = DH(besk, apk)
  anahtarVerisi = HKDF(zincirAnahtarı, paylaşılanGizli, "", 64)
  zincirAnahtarı = anahtarVerisi[0:31]

  // AEAD parametreleri
  k = anahtarVerisi[32:63]
  n = 0
  ad = h
  şifrelenmişMetin = ENCRYPT(k, n, ZEROLEN, ad)

  "se" mesaj deseninin sonu.

  // MixHash(şifrelenmişMetin)
  h = SHA256(h || şifrelenmişMetin)

  zincirAnahtarı aşağıdaki ratchet'ta kullanılır.


```


Yük Bölümü Şifreli İçerik için KDF
````````````````````````````````````````

Bu, ilk Mevcut Oturum mesajının altında çalışır,
ancak ayrıca NSR mesajına bağlamak için yukarıdaki hash'i kullanır.


```text

// split()
  anahtarVerisi = HKDF(zincirAnahtarı, ZEROLEN, "", 64)
  k_ab = anahtarVerisi[0:31]
  k_ba = anahtarVerisi[32:63]
  tagset_ab = DH_INITIALIZE(zincirAnahtarı, k_ab)
  tagset_ba = DH_INITIALIZE(zincirAnahtarı, k_ba)

  // AEAD parametreleri için Yeni Oturum Yanıtı yükü
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  şifrelenmişMetin = ENCRYPT(k, n, payload, ad)

```


### Notlar

Yanıtlarda her bir NS mesajına birden fazla NSR mesajı gönderilebilir,
her bir yanıtın benzersiz geçici anahtarları olur, yanıtın boyutuna bağlı olarak.

Alice ve Bob'un her NS ve NSR mesajı için birbirinden farklı geçici 
anahtarlar kullanmaları gereklidir.

Alice, Bob'un NSR mesajlarından birini aldıktan sonra 
Mevcut Oturum mesajları göndermelidir,
ve Bob, Alice'den bir ES mesajı aldıktan sonra ES mesajlarını göndermelidir.

Alice ve Bob'un NSR yük bölümünün KDF sonuçları
oturuma-zin şifreli DH Ratchet DP'nin başlangıçlarıdır.

Bob ve Alice için ES mesajları alındıktan sonra gelen herhangi bir başka oturum
derhal silinmelidir.


### 1h) Mevcut oturum formatı

Oturum etiketi (8 bayt)
Şifrelenmiş veriler ve MAC (aşağıdaki bölümde 3 incelenecektir)


Format
```````
Şifreli:

```dataspec

+----+----+----+----+----+----+----+----+
  |       Oturum Etiketi                   |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                  +
  |       ChaCha20 şifreli veri           |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Kimlik Doğrulama Kodu |
  +              (MAC)                    +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Oturum Etiketi :: 8 bayt, açık metin

  Yük Bölümü şifreli veriler :: kalan veriler eksi 16 bayt

  MAC :: Poly1305 mesaj kimlik doğrulama kodu, 16 bayt


```


Yük
```````
Şifreli uzunluk verilerin kalanıdır.
Açılmış uzunluk, şifreli uzunluktan 16 daha azdır.
Format ve gereksinimler için yük bölümüne bakın.


KDF
```

```text

Bkz. AAZD bölümü aşağıda.

  // Mevcut Oturum yükü için AEAD parametreleri
  k = Bu oturum etiketiyle ilişkili 32 baytlık oturum anahtarı
  n = Mevcut zincirdeki mesaj numarası N, ilgili Oturum Etiketinden alınan.
  ad = Oturum etiketi, 8 bayt
  şifrelenmişMetin = ENCRYPT(k, n, payload, ad)

```



### 2) ECIES-X25519


Format: 32 bayt ortak ve özel anahtarlar, küçük endian.

Gerekçelendirme: [NTCP2](/en/docs/transport/ntcp2/) içinde kullanılır.



### 2a) Elligator2

Standart Noise el sıkışmalarında, her iki yönde de ilk el sıkışma mesajları,
şifrelenmiş olmayan geçici anahtarlarla başlar.
Geçerli X25519 anahtarlarının rastgelelerden ayırt edilebilir olması nedeniyle,
bir kişinin araya girmesi bu mesajları Mevcut Oturum mesajlarından ayırt edebilir.
[NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/)) içinde, [NTCP2](/en/docs/transport/ntcp2/) 'de kullanılmayan bir yerde [Elligator2](https://elligator.org/) ilavel bir kararla,
anahtarı bulanıklaştırmak için bant dışında statik bir anahtar kullanılmıştır.
Ancak,
tehdit modeli burada farklıdır; başka bir MitM adlı mesajın hedefini doğrulamanı ve 
başlangıç el sıkışma mesajlarının Mevcut Oturum mesajlarından ayırt edilmesini önlemek istiyoruz.

Bu nedenle, [Elligator2](https://elligator.org/) Yeni Oturum ve Yeni Oturum Yanıtı mesajlarındaki geçici anahtarları dönüştürmek
için kullanılır, böylece bunlar üniform rastgele dizilerden ayırt edilemez hale gelir.



Format
``````

32 bayt ortak ve özel anahtarlar.
Kodlanmış anahtarlar küçük endian'dır.

[Elligator2](https://elligator.org/) içinde tanımlandığı gibi, kodlanmış anahtarlar 254 rastgele bitten ayırt edilemez.
256 rastgele bite (32 bayt) gerektiririz. Bu nedenle 
kodlama ve kod çözme aşağıdaki şekilde tanımlanmıştır:

Kodlama:

```text

ENCODE_ELG2() Tanımı

  // Elligator2 spesifikasyonunda tanımlandığı gibi kodlayın
  kodluAnahtar = kodla(pubkey)
  // MSB'ye 2 rastgele bitten ile OR yap                              

  rastgeleBayt = CSRNG(1)
  kodluAnahtar[31] |= (rastgeleBayt & 0xc0)

```


Kod çözme:

```text

DECODE_ELG2() Tanımı

  // MSB'den 2 rastgele biti maskeleyin
  kodluAnahtar[31] &= 0x3f
  // Elligator2 spesifikasyonunda tanımlandığı gibi dekodlayın
  pubkey = kod çöz(kodluAnahtar)

```




Gerekçelendirme
````````````````

OBEP ve IBGW'nin trafiği sınıflandırmasını önlemek için gereklidir.


Notlar
``````````

Elligator2 ortalama anahtar üretim süresini iki katına çıkarır, çünkü
rastgele özel anahtarların yarısı, Elligator2 kodlaması için uygun ortak anahtarlarla sonuçlanmaz.
Ayrıca, anahtar üretim süresi bir üssel dağılımla sınırsızdır,
çünkü anahtar çiftleri uygun bir şekilde bulunana kadar üretici
tekrar tekrar denemek zorundadır.

Bu üst veri, uygun anahtarları elde tutmak için bir havuz
oluşturmak için önceden anahtar üretimi yaparak ve ayrı bir
işlem sırasında yönetilebilir.

Üretici, uygunluk sağlamak için ENCODE_ELG2()
fonksiyonunu uygular.
Bu nedenle, üretici ENCODE_ELG2() sonucunu
depolamalıdır, böylece daha fazla hesaplama gerektirmez.

Ek olarak, uygun olmayan anahtarlar NTCP2'nin
kullanıldığı anahtarlar havuzuna eklenebilir,
burada Elligator2 kullanılmaz.
Bunun yapılmasının güvenlik sorunları TBD.




### 3) AEAD (ChaChaPoly)

AEAD, [NTCP2](/en/docs/transport/ntcp2/)'de olduğu gibi ChaCha20 ve Poly1305 kullanarak.
Bu [RFC-7539](https://tools.ietf.org/html/rfc7539) ile uyuşur,
TLS [RFC-7905](https://tools.ietf.org/html/rfc7905) 'te benzer şekildenir.



Yeni Oturum ve Yeni Oturum Yanıtı Girişleri
````````````````````````````````````````

Bir AEAD bloğundaki şifreleme/deşifreleme fonksiyonları
için girişler, Yeni Oturum mesajında:

```dataspec

k :: 32 bayt şifreleme anahtarı
       Yukarıdaki Yeni Oturum ve Yeni Oturum Yanıtı KDF'lerine bakın.

  n :: Counter tabanlı nonce, 12 bayt.
       n = 0

  ad :: İlişkili veri, 32 bayt.
        Karışık veri olarak çıkıştan
        mixHash()

  data :: Düz metin verileri, 0 veya daha fazla bayt


```


Mevcut Oturum Girişleri
`````````````````````

Bir MEVCUT oturum mesajındaki şifreleme / deşifreleme fonksiyonları
için girişler:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 bayt oturum anahtarı
       Birlikte gönderilen oturum etiketinden alınmıştır.

  n :: Counter tabanlı nonce, 12 bayt.
       Gönderilirken her mesaj için 0'dan başlatılır ve artırılır.
       Alıcı için, 
       birlikte gönderilen oturum etiketinden alınan 
       değeri kullanarak.
       Son dört bayt her zaman sıfırdır.
       Son sekiz bayt, küçük endian olarak 
       kodlanmış mesaj numarası (n).
       Maksimum değer 65535'tir.
       N bu değere ulaştığında oturum 
       ratchet'lenmelidir.
       Daha yüksek değerler asla kullanılmamalıdır.

  ad :: İlişkili veri
        Oturum etiketi

  data
