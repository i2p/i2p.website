---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Kapatıldı"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Not

Ağ dağıtımı ve test süreci devam ediyor. Küçük revizyonlara tabi olabilir. Resmi spesifikasyon için [SPEC](/docs/specs/ecies/) bölümüne bakınız.

Aşağıdaki özellikler 0.9.46 sürümü itibariyle uygulanmamıştır:

- MessageNumbers, Options ve Termination blokları
- Protokol katmanı yanıtları
- Sıfır statik anahtar
- Multicast

## Genel Bakış

Bu, I2P'nin başlangıcından bu yana ilk yeni uçtan uca şifreleme türü için bir öneridir ve ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/) sistemini değiştirmeyi amaçlamaktadır.

Aşağıdaki önceki çalışmalara dayanır:

- Ortak yapılar spec [Common Structures](/docs/specs/common-structures/)
- LS2 dahil [I2NP](/docs/specs/i2np/) spec
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) yeni asimetrik kripto genel bakış
- Düşük seviye kripto genel bakış [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposal 111](/proposals/111-ntcp-2/)
- 123 Yeni netDb Girişleri
- 142 Yeni Kripto Şablonu
- [Noise](https://noiseprotocol.org/noise.html) protokolü
- [Signal](https://signal.org/docs/) çift mandal algoritması

Amaç, uçtan uca, hedeften hedefe iletişim için yeni şifreleme desteği sağlamaktır.

Tasarım, Signal'in çift mandal mekanizmasını içeren bir Noise handshake ve veri aşaması kullanacaktır.

Bu öneriде Signal ve Noise'a yapılan tüm referanslar yalnızca arka plan bilgisi içindir. Bu öneriyi anlamak veya uygulamak için Signal ve Noise protokollerini bilmek gerekli değildir.

### Current ElGamal Uses

Gözden geçirmek gerekirse, ElGamal 256-baytlık public key'ler aşağıdaki veri yapılarında bulunabilir. Ortak yapılar spesifikasyonuna başvurun.

- Bir Router Identity içinde
  Bu, router'ın şifreleme anahtarıdır.

- Bir Destination içinde
  Destination'ın public key'i, 0.6 sürümünde devre dışı bırakılan eski i2cp-to-i2cp şifreleme için kullanılıyordu, şu anda kullanılmamaktadır, yalnızca kullanımdan kaldırılmış olan LeaseSet şifreleme için IV olarak kullanılır.
  Bunun yerine LeaseSet içindeki public key kullanılır.

- Bir LeaseSet içinde
  Bu, hedefin şifreleme anahtarıdır.

- Bir LS2'de
  Bu, hedefin şifreleme anahtarıdır.

### EncTypes in Key Certs

Gözden geçirmek gerekirse, signature türleri desteğini eklediğimizde encryption türleri desteğini de ekledik. Encryption türü alanı hem Destinations hem de RouterIdentities'de her zaman sıfırdır. Bunu değiştirip değiştirmeyeceği henüz belirlenmemiştir (TBD). Ortak yapılar spesifikasyonuna başvurun [Common Structures](/docs/specs/common-structures/).

### Mevcut ElGamal Kullanımları

Gözden geçirmek gerekirse, ElGamal'ı şunlar için kullanırız:

1) Tunnel Build mesajları (anahtar RouterIdentity içindedir)    Değiştirme bu öneride kapsanmamaktadır.    Öneri 152'ye bakın [Öneri 152](/proposals/152-ecies-tunnels).

2) netDb ve diğer I2NP mesajlarının router'dan router'a şifrelenmesi (Anahtar RouterIdentity içinde)    Bu öneriye bağlıdır.    1) için de bir öneri gerektirir, ya da anahtarı RI seçeneklerine koymak gerekir.

3) İstemci Uçtan Uca ElGamal+AES/SessionTag (anahtar LeaseSet içindedir, Destination anahtarı kullanılmaz)    Değiştirme bu öneride KAPSAMLIDIR.

4) NTCP1 ve SSU için Ephemeral DH    Değiştirme bu öneride ele alınmamaktadır.    NTCP2 için öneri 111'e bakınız.    SSU2 için mevcut öneri yoktur.

### Key Cert'lerde EncTypes

- Geriye dönük uyumlu
- LS2 gerektirir ve onun üzerine inşa edilir (öneri 123)
- NTCP2 için eklenen yeni kripto veya temel öğeleri kullanır (öneri 111)
- Destek için yeni kripto veya temel öğe gerektirmez
- Kripto ve imzalama arasındaki ayrışmayı korur; mevcut ve gelecekteki tüm sürümleri destekler
- Destinasyonlar için yeni kripto özelliğini etkinleştirir
- Router'lar için yeni kripto özelliğini etkinleştirir, ancak yalnızca garlic mesajlar için - tunnel oluşturma ayrı bir öneri olacaktır
- 32-byte ikili destinasyon hash'lerine dayanan hiçbir şeyi bozmaz, örneğin bittorrent
- Ephemeral-static DH kullanarak 0-RTT mesaj teslimini korur
- Bu protokol katmanında mesajların tamponlanması / sıraya alınmasını gerektirmez;
  yanıt beklemeden her iki yönde sınırsız mesaj teslimini desteklemeye devam eder
- 1 RTT sonrası ephemeral-ephemeral DH'ye yükseltir
- Sıra dışı mesajların işlenmesini korur
- 256-bit güvenliği korur
- Forward secrecy ekler
- Kimlik doğrulama ekler (AEAD)
- ElGamal'dan çok daha CPU-verimli
- DH'yi verimli hale getirmek için Java jbigi'ye bağımlı olmaz
- DH işlemlerini minimize eder
- ElGamal'dan çok daha bant genişliği-verimli (514 byte ElGamal blok)
- İstenirse aynı tunnel üzerinde yeni ve eski kripto desteği
- Alıcı, aynı tunnel'dan gelen yeni ve eski kriptoyu verimli şekilde ayırt edebilir
- Diğerleri yeni, eski veya gelecekteki kriptoyu ayırt edemez
- Yeni vs. Mevcut Oturum uzunluğu sınıflandırmasını elimine eder (padding desteği)
- Yeni I2NP mesajları gerektirmez
- AES payload'daki SHA-256 checksum'u AEAD ile değiştirir
- Gönderme ve alma oturumlarının bağlanmasını destekler, böylece
  onaylar protokol içinde gerçekleşebilir, yalnızca bant dışı değil.
  Bu ayrıca yanıtların hemen forward secrecy sahibi olmasını sağlar.
- CPU yükü nedeniyle şu anda yapmadığımız belirli mesajların (RouterInfo stores)
  uçtan uca şifrelenmesini mümkün kılar.
- I2NP Garlic Message veya Garlic Message Delivery Instructions
  formatını değiştirmez.
- Garlic Clove Set ve Clove formatlarında kullanılmayan veya gereksiz alanları elimine eder.

Session tag'ler ile ilgili çeşitli sorunları ortadan kaldırır, bunlar şunlardır:

- İlk yanıta kadar AES kullanamama
- Tag tesliminin varsayılması durumunda güvenilmezlik ve durma
- Bant genişliği verimsizliği, özellikle ilk teslimat sırasında
- Tag'leri saklamak için büyük alan verimsizliği
- Tag'leri teslim etmek için büyük bant genişliği ek yükü
- Son derece karmaşık, uygulaması zor
- Çeşitli kullanım durumları için ayarlaması zor
  (streaming vs. datagram, sunucu vs. istemci, yüksek vs. düşük bant genişliği)
- Tag teslimi nedeniyle bellek tükenme güvenlik açıkları

### Asimetrik Kripto Kullanımları

- LS2 format değişiklikleri (öneri 123 tamamlandı)
- Yeni DHT rotasyon algoritması veya paylaşımlı rastgele üretim
- Tunnel oluşturma için yeni şifreleme.
  Öneri 152'ye bakın [Proposal 152](/proposals/152-ecies-tunnels).
- Tunnel katman şifrelemesi için yeni şifreleme.
  Öneri 153'e bakın [Proposal 153](/proposals/153-chacha20-layer-encryption).
- I2NP DLM / DSM / DSRM mesajlarının şifreleme, iletim ve alım yöntemleri.
  Değiştirilmiyor.
- LS1'den LS2'ye veya ElGamal/AES'den bu öneriye iletişim desteklenmiyor.
  Bu öneri çift yönlü bir protokoldür.
  Hedefler aynı tunnel'ları kullanarak iki leaseSet yayınlayarak
  veya her iki şifreleme türünü LS2'ye koyarak geriye dönük uyumluluğu yönetebilir.
- Tehdit modeli değişiklikleri
- Uygulama detayları burada tartışılmıyor ve her projeye bırakılıyor.
- (İyimser) Multicast desteği için uzantı veya kanca ekleme

### Hedefler

ElGamal/AES+SessionTag yaklaşık 15 yıldır tek uçtan uca protokolümüz olmuş durumda, protokolde esasen hiçbir değişiklik yapılmadan. Artık daha hızlı kriptografik primitifler mevcut. Protokolün güvenliğini artırmamız gerekiyor. Ayrıca protokolün bellek ve bant genişliği yükünü minimize etmek için buluşsal stratejiler ve geçici çözümler geliştirdik, ancak bu stratejiler kırılgan, ayarlaması zor ve protokolü daha da kırılmaya eğilimli hale getirerek oturumun düşmesine neden oluyor.

Yaklaşık aynı zaman dilimi boyunca, ElGamal/AES+SessionTag spesifikasyonu ve ilgili dokümantasyon, session tag'lerinin teslim edilmesinin ne kadar bant genişliği pahalısı olduğunu açıklamış ve session tag teslimatının "senkronize PRNG" ile değiştirilmesini önermiştir. Senkronize bir PRNG, ortak bir seed'den türetilmiş olarak her iki uçta da aynı tag'leri deterministik olarak üretir. Senkronize bir PRNG aynı zamanda "ratchet" olarak da adlandırılabilir. Bu öneri (nihayet) söz konusu ratchet mekanizmasını belirler ve tag teslimatını ortadan kaldırır.

Oturum etiketlerini oluşturmak için bir ratchet (senkronize PRNG) kullanarak, New Session mesajında ve gerektiğinde sonraki mesajlarda oturum etiketlerini göndermenin ek yükünü ortadan kaldırıyoruz. 32 etiketlik tipik bir etiket seti için bu 1KB'dir. Bu aynı zamanda gönderen tarafta oturum etiketlerinin saklanmasını ortadan kaldırır, böylece depolama gereksinimlerini yarıya indirir.

Key Compromise Impersonation (KCI) saldırılarından kaçınmak için Noise IK desenine benzer tam çift yönlü bir el sıkışma gereklidir. [NOISE](https://noiseprotocol.org/noise.html)'daki Noise "Payload Security Properties" tablosuna bakın. KCI hakkında daha fazla bilgi için şu makaleye bakın: https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Hedefler Dışında / Kapsam Dışı

Tehdit modeli NTCP2'den (öneri 111) biraz farklıdır. MitM düğümleri OBEP ve IBGW'dir ve floodfill'lerle işbirliği yaparak mevcut veya geçmiş küresel NetDB'nin tam görünümüne sahip oldukları varsayılır.

Amaç, bu MitM'lerin trafiği yeni ve Mevcut Oturum mesajları olarak veya yeni kripto vs. eski kripto olarak sınıflandırmasını önlemektir.

## Detailed Proposal

Bu öneri, ElGamal/AES+SessionTags'i değiştirmek için yeni bir uçtan uca protokol tanımlar. Tasarım, Signal'in çift ratchet'ini içeren bir Noise handshake ve veri aşaması kullanacaktır.

### Gerekçe

Protokolün yeniden tasarlanması gereken beş bölümü vardır:

- 1) Yeni ve Mevcut Oturum konteyner formatları
  yeni formatlarla değiştirilir.
- 2) ElGamal (256 bayt genel anahtarlar, 128 bayt özel anahtarlar)
  ECIES-X25519 (32 bayt genel ve özel anahtarlar) ile değiştirilir
- 3) AES,
  AEAD_ChaCha20_Poly1305 (aşağıda ChaChaPoly olarak kısaltılmıştır) ile değiştirilir
- 4) SessionTags, temelde kriptografik, senkronize bir PRNG olan
  ratchet'larla değiştirilir.
- 5) ElGamal/AES+SessionTags spesifikasyonunda tanımlandığı şekliyle AES payload,
  NTCP2'dekine benzer bir blok formatıyla değiştirilir.

Beş değişikliğin her birinin aşağıda kendi bölümü bulunmaktadır.

### Tehdit Modeli

Mevcut I2P router uygulamaları, şu anda kullanılan I2P protokolleri için gerekli olmayan aşağıdaki standart kriptografik primitifler için uygulamalar gerektirecektir:

- ECIES (ancak bu temelde X25519'dur)
- Elligator2

Henüz [NTCP2](/docs/specs/ntcp2/) ([Öneri 111](/proposals/111-ntcp-2/)) uygulamayan mevcut I2P router uygulamalarının ayrıca şunlar için uygulamalara ihtiyacı olacaktır:

- X25519 anahtar üretimi ve DH
- AEAD_ChaCha20_Poly1305 (aşağıda ChaChaPoly olarak kısaltılmıştır)
- HKDF

### Crypto Type

Kripto tipi (LS2'de kullanılan) 4'tür. Bu, little-endian 32-byte X25519 public key'ini ve burada belirtilen uçtan uca protokolünü gösterir.

Crypto türü 0 ElGamal'dır. Crypto türleri 1-3, ECIES-ECDH-AES-SessionTag için ayrılmıştır, bkz. öneri 145 [Öneri 145](/proposals/145-ecies).

### Kriptografik Tasarımın Özeti

Bu öneri, Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 34, 2018-07-11) tabanlı gereksinimleri sağlar. Noise, [SSU](/docs/legacy/ssu/) protokolünün temelini oluşturan Station-To-Station protokolü [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) ile benzer özelliklere sahiptir. Noise terminolojisinde Alice başlatıcı, Bob ise yanıtlayıcıdır.

Bu öneri Noise protokolü Noise_IK_25519_ChaChaPoly_SHA256 tabanlıdır. (İlk anahtar türetme fonksiyonu için gerçek tanımlayıcı, I2P uzantılarını belirtmek için "Noise_IKelg2_25519_ChaChaPoly_SHA256"'dır - aşağıdaki KDF 1 bölümüne bakın) Bu Noise protokolü aşağıdaki ilkelleri kullanır:

- Interactive Handshake Pattern: IK
  Alice statik anahtarını hemen Bob'a iletir (I)
  Alice Bob'un statik anahtarını zaten bilir (K)

- Tek Yönlü Handshake Kalıbı: N
  Alice statik anahtarını Bob'a iletmez (N)

- DH Function: X25519
  [RFC-7748](https://tools.ietf.org/html/rfc7748)'de belirtildiği gibi 32 bayt anahtar uzunluğuna sahip X25519 DH.

- Cipher Function: ChaChaPoly
  [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi AEAD_CHACHA20_POLY1305.
  İlk 4 baytı sıfıra ayarlanmış 12 baytlık nonce.
  [NTCP2](/docs/specs/ntcp2/)'deki ile aynı.

- Hash Function: SHA256
  I2P'de zaten yaygın olarak kullanılan standart 32-byte hash.

### I2P için Yeni Kriptografik İlkeler

Bu öneri, Noise_IK_25519_ChaChaPoly_SHA256'ya aşağıdaki geliştirmeleri tanımlar. Bunlar genellikle [NOISE](https://noiseprotocol.org/noise.html) bölüm 13'teki yönergeleri takip eder.

1) Açık metin geçici anahtarlar [Elligator2](https://elligator.cr.yp.to/) ile kodlanır.

2) Yanıt, düz metin etiketi ile öneklenir.

3) Payload formatı mesaj 1, 2 ve veri aşaması için tanımlanmıştır. Tabii ki, bu Noise'da tanımlanmamıştır.

Tüm mesajlar bir [I2NP](/docs/specs/i2np/) Garlic Message başlığı içerir. Veri aşaması, Noise veri aşamasına benzer ancak onunla uyumlu olmayan şifreleme kullanır.

### Kripto Türü

Handshake'ler [Noise](https://noiseprotocol.org/noise.html) handshake kalıplarını kullanır.

Aşağıdaki harf eşleme kullanılır:

- e = tek kullanımlık ephemeral anahtar
- s = statik anahtar
- p = mesaj yükü

Tek kullanımlık ve Unbound oturumları Noise N desenine benzer.

```

<- s
  ...
  e es p ->

```
Bound oturumları Noise IK desenine benzer.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

Mevcut ElGamal/AES+SessionTag protokolü tek yönlüdür. Bu katmanda, alıcı bir mesajın nereden geldiğini bilmez. Giden ve gelen oturumlar ilişkilendirilmez. Onaylamalar, clove içinde bir DeliveryStatusMessage (GarlicMessage içine sarılmış) kullanılarak bant dışı olarak yapılır.

Tek yönlü bir protokolde önemli bir verimsizlik vardır. Herhangi bir yanıt da pahalı bir 'New Session' mesajı kullanmak zorundadır. Bu durum daha yüksek bant genişliği, CPU ve bellek kullanımına neden olur.

Tek yönlü bir protokolde güvenlik zayıflıkları da vardır. Tüm oturumlar ephemeral-static DH'ye dayanır. Geri dönüş yolu olmadan, Bob'un statik anahtarını ephemeral anahtara "ratchet" etmesinin bir yolu yoktur. Bir mesajın nereden geldiğini bilmeden, alınan ephemeral anahtarı giden mesajlar için kullanmanın bir yolu yoktur, bu nedenle ilk yanıt da ephemeral-static DH kullanır.

Bu öneri için, çift yönlü bir protokol oluşturmak üzere iki mekanizma tanımlıyoruz - "eşleştirme" ve "bağlama". Bu mekanizmalar artan verimlilik ve güvenlik sağlar.

### Framework'e Eklemeler

ElGamal/AES+SessionTags ile aynı şekilde, tüm gelen ve giden oturumlar belirli bir bağlamda olmalıdır; ya router'ın bağlamında ya da belirli bir yerel hedefin bağlamında. Java I2P'de bu bağlam Session Key Manager olarak adlandırılır.

Oturumlar bağlamlar arasında paylaşılmamalıdır, çünkü bu çeşitli yerel hedefler arasında veya yerel bir hedef ile router arasında korelasyona izin verir.

Belirli bir hedef hem ElGamal/AES+SessionTags hem de bu öneriyi desteklediğinde, her iki oturum türü de bir bağlamı paylaşabilir. Aşağıda 1c) bölümüne bakın.

### Handshake Kalıpları

Başlatıcıda (Alice) bir giden oturum oluşturulduğunda, yanıt beklenmediği durumlar dışında (örn. ham datagramlar) yeni bir gelen oturum oluşturulur ve giden oturumla eşleştirilir.

Yeni bir gelen oturum, yanıt istenmediği durumlar dışında (örn. ham datagramlar) her zaman yeni bir giden oturum ile eşleştirilir.

Bir yanıt isteniyorsa ve uzak uç hedef veya router'a bağlıysa, bu yeni giden oturum o hedef veya router'a bağlanır ve o hedef veya router'a olan önceki giden oturumu değiştirir.

Gelen ve giden oturumları eşleştirmek, DH anahtarlarını ratcheting yapabilme yeteneğine sahip çift yönlü bir protokol sağlar.

### Oturumlar

Belirli bir hedefe veya router'a yalnızca bir giden oturum vardır. Belirli bir hedef veya router'dan birden fazla mevcut gelen oturum olabilir. Genellikle, yeni bir gelen oturum oluşturulduğunda ve bu oturum üzerinde trafik alındığında (bu bir ACK görevi görür), diğerleri yaklaşık bir dakika içinde nispeten hızlı bir şekilde sona ermek üzere işaretlenir. Önceki gönderilen mesajlar (PN) değeri kontrol edilir ve önceki gelen oturumda (pencere boyutu dahilinde) alınmamış mesaj yoksa, önceki oturum derhal silinebilir.

Kaynak noktasında (Alice) bir giden oturum oluşturulduğunda, uzak uç Destination'a (Bob) bağlanır ve eşleştirilmiş herhangi bir gelen oturum da uzak uç Destination'a bağlanır. Oturumlar ratchet işlemi gerçekleştirirken, uzak uç Destination'a bağlı kalmaya devam ederler.

Alıcıda (Bob) bir gelen oturum oluşturulduğunda, Alice'in seçimine bağlı olarak uzak uç Destination'a (Alice) bağlanabilir. Alice, New Session mesajında bağlama bilgisini (statik anahtarını) dahil ederse, oturum o destination'a bağlanacak ve aynı Destination'a bağlı bir giden oturum oluşturulacaktır. Oturumlar ratchet işlemi gerçekleştirirken, uzak uç Destination'a bağlı olmaya devam ederler.

### Oturum Bağlamı

Yaygın, akış durumu için Alice ve Bob'un protokolü şu şekilde kullanmasını bekliyoruz:

- Alice, yeni outbound oturumunu yeni bir inbound oturumuyla eşleştirir; her ikisi de uzak uç hedefine (Bob) bağlanır.
- Alice, bağlama bilgilerini ve imzayı, ayrıca yanıt talebini Bob'a gönderilen
  New Session mesajına dahil eder.
- Bob, yeni inbound oturumunu yeni bir outbound oturumuyla eşleştirir; her ikisi de uzak uç hedefine (Alice) bağlanır.
- Bob, eşleştirilmiş oturumda Alice'e yeni bir DH anahtarına ratchet ile birlikte yanıt (ack) gönderir.
- Alice, Bob'un yeni anahtarıyla yeni bir outbound oturuma ratchet yapar; bu oturum mevcut inbound oturumuyla eşleştirilir.

Gelen bir oturumu uzak uç Destination'a bağlayarak ve gelen oturumu aynı Destination'a bağlı giden bir oturumla eşleştirerek, iki önemli fayda elde ederiz:

1) Bob'tan Alice'e gelen ilk yanıt ephemeral-ephemeral DH kullanır

2) Alice, Bob'un yanıtını aldıktan ve ratchet işlemini yaptıktan sonra, Alice'ten Bob'a gönderilen tüm sonraki mesajlar ephemeral-ephemeral DH kullanır.

### Gelen ve Giden Oturumları Eşleştirme

ElGamal/AES+SessionTags'da, bir LeaseSet garlic clove olarak paketlendiğinde veya etiketler iletildiğinde, gönderen router bir ACK talep eder. Bu, bir DeliveryStatus Mesajı içeren ayrı bir garlic clove'dur. Ek güvenlik için, DeliveryStatus Mesajı bir Garlic Mesajına sarılır. Bu mekanizma protokol perspektifinden bant-dışıdır.

Yeni protokolde, gelen ve giden oturumlar eşleştirildiği için ACK'ları bant içinde tutabiliriz. Ayrı bir clove gerekliliği yoktur.

Açık bir ACK, basitçe I2NP bloğu olmayan bir Mevcut Oturum mesajıdır. Ancak, çoğu durumda, ters trafik olduğu için açık bir ACK'den kaçınılabilir. Uygulamaların, streaming veya uygulama katmanına yanıt verme zamanı tanımak için açık bir ACK göndermeden önce kısa bir süre (belki yüz ms) beklemesi arzu edilebilir.

Uygulamalar ayrıca herhangi bir ACK gönderimi işlemini I2NP bloğu işlenene kadar ertelemek zorunda kalacaktır, çünkü Garlic Message bir lease set içeren Database Store Message içerebilir. ACK'yi yönlendirmek için güncel bir lease set gerekli olacaktır ve bağlayıcı statik anahtarı doğrulamak için uzak uç hedef (lease set içinde bulunan) gerekli olacaktır.

### Oturum ve Hedef Bağlama

Giden oturumlar her zaman gelen oturumlardan önce sona ermelidir. Bir giden oturum sona erdiğinde ve yeni bir oturum oluşturulduğunda, yeni bir eşleştirilmiş gelen oturum da oluşturulacaktır. Eski bir gelen oturum varsa, bunun sona ermesine izin verilecektir.

### Bağlama ve Eşleştirmenin Faydaları

TBD

### Mesaj ACK'leri

Kullanılan kriptografik yapı taşlarına karşılık gelen aşağıdaki fonksiyonları tanımlıyoruz.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Oturum Zaman Aşımları

### Multicast

[I2NP](/docs/specs/i2np/) spesifikasyonunda belirtilen Garlic Message aşağıdaki gibidir. Ara düğümlerin yeni ve eski kriptoyu ayırt edememesi bir tasarım hedefi olduğundan, uzunluk alanı gereksiz olsa bile bu format değiştirilemez. Format tam 16 baytlık başlıkla gösterilmiştir, ancak kullanılan taşıma protokolüne bağlı olarak gerçek başlık farklı bir formatta olabilir.

Şifrelendiğinde veri, Clove Set olarak da bilinen bir dizi Garlic Clove ve ek veri içerir.

Ayrıntılar ve tam spesifikasyon için [I2NP](/docs/specs/i2np/) bölümüne bakın.

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### Tanımlar

Mevcut mesaj formatı, 15 yıldan fazla süredir kullanılan ElGamal/AES+SessionTags'dir. ElGamal/AES+SessionTags'de iki mesaj formatı bulunmaktadır:

1) Yeni oturum: - 514 bayt ElGamal bloğu - AES bloğu (minimum 128 bayt, 16'nın katı)

2) Mevcut oturum: - 32 bayt Session Tag - AES bloğu (minimum 128 bayt, 16'nın katı)

128'e minimum padding Java I2P'de uygulandığı gibidir ancak alımda zorlanmaz.

Bu mesajlar, bir uzunluk alanı içeren I2NP garlic mesajında kapsüllenir, böylece uzunluk bilinir.

Mod-16 olmayan bir uzunluğa tanımlanmış hiçbir padding bulunmadığını, bu yüzden New Session'ın her zaman (mod 16 == 2) ve Existing Session'ın her zaman (mod 16 == 0) olduğunu unutmayın. Bunu düzeltmemiz gerekiyor.

Alıcı önce ilk 32 baytı Session Tag olarak arama yapmaya çalışır. Bulursa, AES bloğunu çözer. Bulamazsa ve veri en az (514+16) uzunluktaysa, ElGamal bloğunu çözmeye çalışır ve başarılı olursa, AES bloğunu çözer.

### 1) Mesaj formatı

Signal Double Ratchet'te, başlık şunları içerir:

- DH: Mevcut ratchet genel anahtarı
- PN: Önceki zincir mesaj uzunluğu
- N: Mesaj Numarası

Signal'in "sending chains"leri kabaca bizim tag setlerimize eşdeğerdir. Bir session tag kullanarak, bunun çoğunu ortadan kaldırabiliriz.

New Session'da, şifrelenmemiş başlığa yalnızca public key'i koyarız.

Mevcut Oturumda, başlık için bir oturum etiketi kullanırız. Oturum etiketi, mevcut ratchet genel anahtarı ve mesaj numarası ile ilişkilendirilir.

Hem yeni hem de Mevcut Oturum'da, PN ve N şifrelenmiş gövdede bulunur.

Signal'de her şey sürekli olarak ratcheting yapıyor. Yeni bir DH public key, alıcının ratchet yapmasını ve yeni bir public key geri göndermesini gerektiriyor, bu da alınan public key için ack görevi görüyor. Bu bizim için çok fazla DH işlemi olurdu. Bu yüzden alınan key'in ack'ini ve yeni bir public key'in iletimini ayırıyoruz. Yeni DH public key'den üretilen session tag kullanan herhangi bir mesaj bir ACK oluşturur. Yeni bir public key'i yalnızca rekey yapmak istediğimizde iletiriz.

DH'nin ratchet yapması gereken maksimum mesaj sayısı 65535'tir.

Bir session key'i teslim ederken, session tag'lerini de teslim etmek zorunda kalmak yerine "Tag Set"i ondan türetiyoruz. Bir Tag Set 65536 tag'e kadar olabilir. Ancak alıcılar, tüm olası tag'leri bir kerede oluşturmak yerine "look-ahead" stratejisi uygulamalıdır. Alınan son geçerli tag'den sonra en fazla N tag oluşturun. N en fazla 128 olabilir, ancak 32 veya daha az daha iyi bir seçim olabilir.

### Mevcut Mesaj Formatının İncelemesi

Yeni Oturum Tek Kullanımlık Açık Anahtar (32 bayt) Şifrelenmiş veri ve MAC (kalan baytlar)

New Session mesajı gönderenin statik genel anahtarını içerebilir veya içermeyebilir. Eğer dahil edilirse, ters oturum bu anahtara bağlanır. Yanıt bekleniyorsa, yani streaming ve yanıtlanabilir datagramlar için statik anahtar dahil edilmelidir. Ham datagramlar için dahil edilmemelidir.

New Session mesajı, tek yönlü Noise [NOISE](https://noiseprotocol.org/noise.html) "N" desenine (statik anahtar gönderilmezse) veya iki yönlü "IK" desenine (statik anahtar gönderilirse) benzerdir.

### Şifrelenmiş Veri Formatı İncelemesi

Uzunluk 96 + payload uzunluğudur. Şifrelenmiş format:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Yeni Oturum Etiketleri ve Signal ile Karşılaştırma

Geçici anahtar 32 bayttır ve Elligator2 ile kodlanır. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesaj için yeni bir anahtar oluşturulur.

### 1a) Yeni oturum formatı

Deşifre edildiğinde, Alice'in X25519 statik anahtarı, 32 bayt.

### 1b) Yeni oturum formatı (bağlama ile)

Şifrelenmiş uzunluk, verinin kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Payload bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerecektir. Format ve ek gereksinimler için aşağıdaki payload bölümüne bakın.

### Yeni Oturum Geçici Anahtarı

Yanıt gerekli değilse, statik anahtar gönderilmez.

Uzunluk 96 + payload uzunluğudur. Şifrelenmiş format:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Statik Anahtar

Alice'in geçici anahtarı. Geçici anahtar 32 bayttır, Elligator2 ile kodlanmış, little endian formatında. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesajla birlikte yeni bir anahtar üretilir.

### Yük

Flags bölümü hiçbir şey içermez. Her zaman 32 bayt uzunluğundadır, çünkü bağlama ile New Session mesajlarındaki statik anahtar ile aynı uzunlukta olmalıdır. Bob, 32 baytın hepsinin sıfır olup olmadığını test ederek bunun bir statik anahtar mı yoksa flags bölümü mü olduğunu belirler.

TODO burada herhangi bir flag gerekli mi?

### 1c) Yeni oturum formatı (bağlama olmadan)

Şifrelenmiş uzunluk verinin geri kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 daha azdır. Payload bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki payload bölümüne bakın.

### Yeni Oturum Geçici Anahtarı

Yalnızca tek bir mesajın gönderilmesi bekleniyorsa, oturum kurulumu veya statik anahtar gerekmez.

Uzunluk 96 + payload uzunluğudur. Şifrelenmiş format:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Flags Bölümü Şifresi Çözülmüş veri

Tek kullanımlık anahtar 32 byte'tır, Elligator2 ile kodlanmış, little endian formatında. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesajla birlikte yeni bir anahtar üretilir.

### Yük Verisi

Flags bölümü hiçbir şey içermez. Her zaman 32 bayttır, çünkü bağlama ile New Session mesajları için statik anahtar ile aynı uzunlukta olmalıdır. Bob, 32 baytın tümünün sıfır olup olmadığını test ederek bunun bir statik anahtar mı yoksa flags bölümü mü olduğunu belirler.

TODO burada herhangi bir flag gerekli mi?

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) Tek seferlik format (bağlama veya oturum yok)

Şifreli uzunluk, verinin kalan kısmıdır. Şifresi çözülmüş uzunluk, şifreli uzunluktan 16 eksiktir. Yük (payload) bir DateTime bloğu içermeli ve genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki yük bölümüne bakın.

### Yeni Oturum Tek Kullanımlık Anahtar

### Flags Bölümü Şifrelenmiş veri

Bu, değiştirilmiş bir protokol adı ile IK için standart [NOISE](https://noiseprotocol.org/noise.html)'dur. Hem IK pattern (bağlı oturumlar) hem de N pattern (bağlı olmayan oturumlar) için aynı başlatıcıyı kullandığımızı unutmayın.

Protokol adı iki nedenden dolayı değiştirilmiştir. İlk olarak, geçici anahtarların Elligator2 ile kodlandığını belirtmek için, ikinci olarak da tag değerini karıştırmak amacıyla ikinci mesajdan önce MixHash() çağrıldığını belirtmek için.

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### Yük

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) Yeni Oturum Mesajı için KDF'ler

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### İlk ChainKey için KDF

Bunun bir Noise "N" kalıbı olduğunu, ancak bağlı oturumlar için kullandığımız aynı "IK" başlatıcısını kullandığımızı unutmayın.

Yeni Oturum mesajları, statik anahtar şifreleri çözülüp tamamının sıfır olup olmadığını belirlemek üzere incelenene kadar Alice'in statik anahtarını içerip içermediği belirlenemez. Bu nedenle, alıcı tüm Yeni Oturum mesajları için "IK" durum makinesini kullanmalıdır. Statik anahtar tamamen sıfırsa, "ss" mesaj desenini atlamalıdır.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### Flags/Static Key Bölümü Şifrelenmiş İçerikler için KDF

Tek bir New Session mesajına yanıt olarak bir veya daha fazla New Session Reply gönderilebilir. Her yanıt, oturum için bir TagSet'ten oluşturulan bir etiketle başlar.

New Session Reply iki bölümden oluşur. İlk bölüm, önüne eklenmiş bir etiketle birlikte Noise IK el sıkışmasının tamamlanmasıdır. İlk bölümün uzunluğu 56 bayttır. İkinci bölüm, veri aşaması yüküdür. İkinci bölümün uzunluğu 16 + yük uzunluğudur.

Toplam uzunluk 72 + payload uzunluğudur. Şifrelenmiş format:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Payload Bölümü için KDF (Alice statik anahtarı ile)

Tag, aşağıdaki DH Initialization KDF'de başlatıldığı şekilde Session Tags KDF'de üretilir. Bu, yanıtı oturumla ilişkilendirir. DH Initialization'dan gelen Session Key kullanılmaz.

### Payload Bölümü için KDF (Alice statik anahtarı olmadan)

Bob'un geçici anahtarı. Geçici anahtar 32 bayttır, Elligator2 ile kodlanmış, little endian formatındadır. Bu anahtar asla yeniden kullanılmaz; yeniden iletimler dahil olmak üzere her mesajla birlikte yeni bir anahtar oluşturulur.

### 1g) Yeni Oturum Yanıt formatı

Şifrelenmiş uzunluk, verinin geri kalanıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Payload genellikle bir veya daha fazla Garlic Clove bloğu içerir. Format ve ek gereksinimler için aşağıdaki payload bölümüne bakın.

### Oturum Etiketi

TagSet'ten bir veya daha fazla etiket oluşturulur, bu TagSet aşağıdaki KDF kullanılarak New Session mesajından gelen chainKey ile başlatılır.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Yeni Oturum Yanıtı Ephemeral Key

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### Yük

Bu, bölünme sonrası ilk Mevcut Oturum mesajı gibidir, ancak ayrı bir etiket olmadan. Ek olarak, payload'ı NSR mesajına bağlamak için yukarıdaki hash'i kullanırız.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### Reply TagSet için KDF

Yanıt boyutuna bağlı olarak, her biri benzersiz geçici anahtarlara sahip birden fazla NSR mesajı gönderilebilir.

Alice ve Bob'un her NS ve NSR mesajı için yeni geçici anahtarlar kullanması gerekir.

Alice, Mevcut Oturum (ES) mesajları göndermeden önce Bob'un NSR mesajlarından birini almak zorundadır ve Bob, ES mesajları göndermeden önce Alice'den bir ES mesajı almak zorundadır.

Bob'un NSR Payload Section'ındaki ``chainKey`` ve ``k`` değerleri, başlangıçtaki ES DH Ratchet'ler için girdi olarak kullanılır (her iki yön için, DH Ratchet KDF'ye bakın).

Bob, yalnızca Alice'den aldığı ES mesajları için Mevcut Oturumları korumalıdır. Oluşturulan diğer tüm gelen ve giden oturumlar (birden fazla NSR için) belirli bir oturum için Alice'in ilk ES mesajını aldıktan hemen sonra yok edilmelidir.

### Yanıt Anahtarı Bölümü Şifrelenmiş İçerikleri için KDF

Session etiketi (8 bayt) Şifreli veri ve MAC (aşağıda bölüm 3'e bakın)

### Payload Bölümü Şifrelenmiş İçerikleri için KDF

Şifrelenmiş:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Notlar

Şifrelenmiş uzunluk, verinin geri kalan kısmıdır. Şifresi çözülmüş uzunluk, şifrelenmiş uzunluktan 16 eksiktir. Format ve gereksinimler için aşağıdaki payload bölümüne bakın.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Mevcut oturum formatı

Format: 32-byte genel ve özel anahtarlar, little-endian.

Gerekçe: [NTCP2](/docs/specs/ntcp2/) içinde kullanılır.

### Format

Standart Noise handshake'lerinde, her yöndeki ilk handshake mesajları düz metin olarak iletilen ephemeral anahtarlarla başlar. Geçerli X25519 anahtarları rastgeleden ayırt edilebildiği için, bir man-in-the-middle bu mesajları rastgele session etiketleriyle başlayan Mevcut Oturum mesajlarından ayırt edebilir. [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/)) içinde, anahtarı gizlemek için band dışı statik anahtar kullanan düşük maliyetli bir XOR fonksiyonu kullandık. Ancak, buradaki tehdit modeli farklıdır; herhangi bir MitM'in trafiğin hedefini doğrulamak veya ilk handshake mesajlarını Mevcut Oturum mesajlarından ayırt etmek için herhangi bir yöntem kullanmasına izin vermek istemiyoruz.

Bu nedenle, New Session ve New Session Reply mesajlarındaki geçici anahtarları dönüştürmek için [Elligator2](https://elligator.cr.yp.to/) kullanılır, böylece bu anahtarlar düzgün rastgele dizgilerden ayırt edilemez hale gelir.

### Yük Verisi

32-byte genel ve özel anahtarlar. Kodlanmış anahtarlar little endian formatındadır.

[Elligator2](https://elligator.cr.yp.to/) içinde tanımlandığı gibi, kodlanmış anahtarlar 254 rastgele bitten ayırt edilemez. Biz 256 rastgele bit (32 bayt) gerektiriyoruz. Bu nedenle, kodlama ve kod çözme aşağıdaki gibi tanımlanır:

Kodlama:

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
Çözme:

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

OBEP ve IBGW'nin trafiği sınıflandırmasını önlemek için gereklidir.

### 2a) Elligator2

Elligator2, anahtar üretim süresini ortalama iki katına çıkarır, çünkü özel anahtarların yarısı Elligator2 ile kodlama için uygun olmayan genel anahtarlarla sonuçlanır. Ayrıca, üretici uygun bir anahtar çifti bulunana kadar yeniden denemeye devam etmek zorunda olduğundan, anahtar üretim süresi üstel dağılımla sınırsızdır.

Bu ek yük, uygun anahtarlardan oluşan bir havuz tutmak için anahtar üretimini önceden, ayrı bir thread'de yaparak yönetilebilir.

Generator, uygunluğu belirlemek için ENCODE_ELG2() fonksiyonunu yapar. Bu nedenle, generator, tekrar hesaplanması gerekmemesi için ENCODE_ELG2() sonucunu saklamalıdır.

Ek olarak, uygun olmayan anahtarlar Elligator2'nin kullanılmadığı [NTCP2](/docs/specs/ntcp2/) için kullanılan anahtar havuzuna eklenebilir. Bunu yapmanın güvenlik sorunları henüz belirlenmemiştir.

### Format

ChaCha20 ve Poly1305 kullanarak AEAD, [NTCP2](/docs/specs/ntcp2/) ile aynı. Bu [RFC-7539](https://tools.ietf.org/html/rfc7539)'a karşılık gelir, bu da TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)'te benzer şekilde kullanılır.

### Gerekçe

Yeni Oturum mesajında bir AEAD bloğu için şifreleme/şifre çözme fonksiyonlarına girişler:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Notlar

Mevcut Oturum mesajında bir AEAD bloğu için şifreleme/şifre çözme fonksiyonlarına girişler:

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

Şifreleme fonksiyonunun çıktısı, deşifreleme fonksiyonunun girdisi:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Yeni Oturum ve Yeni Oturum Yanıtı Girdileri

- ChaCha20 bir akış şifresi olduğundan, düz metinlerin doldurulması gerekmez.
  Ek anahtar akışı baytları atılır.

- Şifre için anahtar (256 bit) SHA256 KDF aracılığıyla kararlaştırılır.
  Her mesaj için KDF'nin ayrıntıları aşağıdaki ayrı bölümlerde yer almaktadır.

- ChaChaPoly çerçeveleri I2NP veri mesajında kapsüllendikleri için bilinen boyuttadır.

- Tüm mesajlar için,
  padding kimlik doğrulaması yapılmış
  veri çerçevesinin içindedir.

### Mevcut Oturum Girdileri

AEAD doğrulamasında başarısız olan tüm alınan veriler atılmalıdır. Hiçbir yanıt döndürülmez.

### Şifrelenmiş Format

[NTCP2](/docs/specs/ntcp2/)'de kullanılır.

### Notlar

Daha önce olduğu gibi session tag'leri hâlâ kullanıyoruz, ancak bunları oluşturmak için ratchet'ler kullanıyoruz. Session tag'lerinin hiç uygulamadığımız bir yeniden anahtarlama seçeneği de vardı. Yani çift ratchet gibi ama ikincisini hiç yapmadık.

Burada Signal'in Double Ratchet'ına benzer bir şey tanımlıyoruz. Session tag'leri deterministik olarak ve alıcı ile gönderici taraflarında özdeş şekilde üretilir.

Simetrik anahtar/etiket ratchet kullanarak, gönderen tarafta session etiketlerini depolamak için gereken bellek kullanımını ortadan kaldırıyoruz. Ayrıca etiket kümelerini göndermenin bant genişliği tüketimini de ortadan kaldırıyoruz. Alıcı tarafındaki kullanım hâlâ önemli, ancak session etiketini 32 bayttan 8 bayta küçülteceğimiz için bunu daha da azaltabiliriz.

Signal'da belirtilen (ve isteğe bağlı olan) başlık şifrelemeyi kullanmıyoruz, bunun yerine oturum etiketleri kullanıyoruz.

DH ratchet kullanarak ileri gizlilik elde ediyoruz, bu hiçbir zaman ElGamal/AES+SessionTags'te uygulanmamıştı.

Not: New Session tek kullanımlık public key, ratchet'ın bir parçası değildir, tek işlevi Alice'in ilk DH ratchet key'ini şifrelemektir.

### AEAD Hata İşleme

Double Ratchet, kaybolmuş veya sıra dışı mesajları her mesaj başlığına bir etiket dahil ederek ele alır. Alıcı etiketin indeksini arar, bu mesaj numarası N'dir. Mesaj bir PN değeri içeren Mesaj Numarası bloğu içeriyorsa, alıcı önceki etiket kümesinde o değerden yüksek olan tüm etiketleri silebilir, aynı zamanda atlanan mesajların daha sonra gelmesi durumunda önceki etiket kümesinden atlanan etiketleri saklayabilir.

### Gerekçe

Bu ratchet'ları uygulamak için aşağıdaki veri yapılarını ve fonksiyonları tanımlıyoruz.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

ETIKET SETİ

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchet'ler

Ratchet'lar ancak Signal'in yaptığı kadar hızlı değil. Alınan anahtarın onayını yeni anahtar oluşturmaktan ayırıyoruz. Tipik kullanımda, Alice ve Bob her biri Yeni Oturumda hemen (iki kez) ratchet yapacak, ancak tekrar ratchet yapmayacaklar.

Bir ratchet'ın tek yön için olduğunu ve o yön için bir Yeni Oturum etiketi / mesaj anahtarı ratchet zinciri oluşturduğunu unutmayın. Her iki yön için de anahtarlar oluşturmak için iki kez ratchet yapmanız gerekir.

Her yeni anahtar oluşturup gönderdiğinizde ratchet yaparsınız. Her yeni anahtar aldığınızda ratchet yaparsınız.

Alice, bağlantısız giden oturum oluştururken bir kez ratchet yapar, gelen oturum oluşturmaz (bağlantısız yanıtlanamaz).

Bob, bağlı olmayan gelen oturum oluştururken bir kez ratchet yapar ve karşılık gelen giden oturum oluşturmaz (unbound yanıtlanamaz).

Alice, Bob'dan New Session Reply (NSR) mesajlarından birini alana kadar Bob'a New Session (NS) mesajları göndermeye devam eder. Daha sonra NSR'nin Payload Section KDF sonuçlarını oturum ratchet'ları için girdi olarak kullanır (bkz. DH Ratchet KDF) ve Existing Session (ES) mesajları göndermeye başlar.

Her alınan NS mesajı için Bob, yanıt Payload Section'ının KDF sonuçlarını yeni gelen ve giden ES DH Ratchet için girdi olarak kullanarak yeni bir inbound session oluşturur.

Gereken her yanıt için, Bob Alice'e payload'da yanıtı içeren bir NSR mesajı gönderir. Bob'un her NSR için yeni ephemeral anahtarlar kullanması gereklidir.

Bob, karşılık gelen outbound oturumunda ES mesajları oluşturup göndermeden önce, inbound oturumlarından birinde Alice'ten bir ES mesajı almalıdır.

Alice, Bob'tan NSR mesajı almak için bir zamanlayıcı kullanmalıdır. Zamanlayıcı süresi dolarsa, oturum kaldırılmalıdır.

KCI ve/veya kaynak tükenmesi saldırısını önlemek için, bir saldırganın Bob'un NSR yanıtlarını düşürerek Alice'in NS mesajları göndermeye devam etmesini sağladığı durumda, Alice zamanlayıcı süre aşımı nedeniyle belirli sayıda yeniden deneme sonrasında Bob'a Yeni Oturum başlatmaktan kaçınmalıdır.

Alice ve Bob, alınan her NextKey bloğu için bir DH ratchet gerçekleştirir.

Alice ve Bob her DH ratchet sonrasında yeni tag setleri ve iki simetrik anahtar ratchet'ı üretir. Belirli bir yöndeki her yeni ES mesajı için, Alice ve Bob oturum tag'ini ve simetrik anahtar ratchet'larını ilerletir.

İlk el sıkışmadan sonra DH ratchet'ların sıklığı implementasyona bağlıdır. Protokol bir ratchet gerekli olmadan önce 65535 mesaj sınırı koyarken, daha sık ratcheting (mesaj sayısı, geçen süre veya her ikisine dayalı) ek güvenlik sağlayabilir.

Bağlı oturumlarda son handshake KDF'den sonra, Bob ve Alice gelen ve giden oturumlar için bağımsız simetrik ve etiket zinciri anahtarları oluşturmak üzere ortaya çıkan CipherState üzerinde Noise Split() fonksiyonunu çalıştırmalıdır.

#### KEY AND TAG SET IDS

Anahtar ve etiket kümesi ID numaraları, anahtarları ve etiket kümelerini tanımlamak için kullanılır. Anahtar ID'leri, NextKey bloklarında gönderilen veya kullanılan anahtarı tanımlamak için kullanılır. Etiket kümesi ID'leri, ACK bloklarında (mesaj numarası ile birlikte) onaylanan mesajı tanımlamak için kullanılır. Hem anahtar hem de etiket kümesi ID'leri tek bir yön için etiket kümelerine uygulanır. Anahtar ve etiket kümesi ID numaraları sıralı olmalıdır.

Her yönde bir oturum için kullanılan ilk etiket kümelerinde, etiket kümesi ID'si 0'dır. Hiçbir NextKey bloğu gönderilmemiştir, bu nedenle anahtar ID'leri yoktur.

Bir DH ratchet başlatmak için, gönderen 0 key ID'si ile yeni bir NextKey bloğu iletir. Alıcı 0 key ID'si ile yeni bir NextKey bloğu ile yanıtlar. Gönderen daha sonra 1 tag set ID'si ile yeni bir tag set kullanmaya başlar.

Sonraki etiket kümeleri benzer şekilde oluşturulur. NextKey değişimlerinden sonra kullanılan tüm etiket kümeleri için, etiket kümesi numarası (1 + Alice'in anahtar kimliği + Bob'un anahtar kimliği) şeklindedir.

Anahtar ve etiket kümesi ID'leri 0'dan başlar ve sıralı olarak artar. Maksimum etiket kümesi ID'si 65535'tir. Maksimum anahtar ID'si 32767'dir. Bir etiket kümesi neredeyse tükendiğinde, etiket kümesi gönderici bir NextKey değişimi başlatmalıdır. 65535 numaralı etiket kümesi neredeyse tükendiğinde, etiket kümesi gönderici bir New Session mesajı göndererek yeni bir oturum başlatmalıdır.

1730'luk bir streaming maksimum mesaj boyutu ile ve yeniden iletim olmadığını varsayarak, tek bir etiket seti kullanarak teorik maksimum veri aktarımı 1730 * 65536 ~= 108 MB'dir. Gerçek maksimum değer, yeniden iletimler nedeniyle daha düşük olacaktır.

Mevcut tüm 65536 etiket seti ile teorik maksimum veri aktarımı, oturum atılıp değiştirilmeden önce, 64K * 108 MB ~= 6.9 TB'dir.

#### DH RATCHET MESSAGE FLOW

Bir tag kümesi için bir sonraki anahtar değişimi, bu tag'lerin gönderici tarafından (outbound tag kümesinin sahibi) başlatılmalıdır. Alıcı (inbound tag kümesinin sahibi) yanıt verecektir. Uygulama katmanında tipik bir HTTP GET trafiği için Bob daha fazla mesaj gönderecek ve anahtar değişimini başlatarak ilk olarak ratchet yapacaktır; aşağıdaki diyagram bunu gösterir. Alice ratchet yaptığında, aynı şey tersine olur.

NS/NSR handshake'inden sonra kullanılan ilk tag seti, tag set 0'dır. Tag set 0 neredeyse tükendiğinde, tag set 1'i oluşturmak için her iki yönde de yeni anahtarların değişimi gerekir. Bundan sonra, yeni anahtar yalnızca bir yönde gönderilir.

Tag set 2'yi oluşturmak için, tag gönderen yeni bir anahtar gönderir ve tag alan onaylama olarak eski anahtarının ID'sini gönderir. Her iki taraf da bir DH yapar.

Tag seti 3'ü oluşturmak için, tag gönderen taraf eski anahtarının ID'sini gönderir ve tag alan taraftan yeni bir anahtar talep eder. Her iki taraf da bir DH yapar.

Sonraki etiket kümeleri, etiket küme 2 ve 3'te olduğu gibi oluşturulur. Etiket küme numarası (1 + gönderici anahtar id'si + alıcı anahtar id'si)'dir.

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
Giden tagset için DH ratchet tamamlandıktan ve yeni bir giden tagset oluşturulduktan sonra, hemen kullanılmalı ve eski giden tagset silinebilir.

Gelen tagset için DH ratchet tamamlandıktan ve yeni bir gelen tagset oluşturulduktan sonra, alıcı her iki tagset'teki etiketleri dinlemeli ve eski tagset'i kısa bir süre sonra, yaklaşık 3 dakika içinde silmelidir.

Aşağıdaki tabloda etiket seti ve anahtar kimliği ilerlemesinin özeti bulunmaktadır. * yeni bir anahtarın oluşturulduğunu gösterir.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Anahtar ve etiket kümesi ID numaraları sıralı olmalıdır.

#### DH INITIALIZATION KDF

Bu, tek bir yön için DH_INITIALIZE(rootKey, k) tanımıdır. Bu fonksiyon bir tagset ve gerektiğinde sonraki bir DH ratchet için kullanılacak "sonraki root key" oluşturur.

DH başlatma işlemini üç yerde kullanıyoruz. İlk olarak, New Session Replies için bir etiket seti oluşturmak amacıyla kullanıyoruz. İkinci olarak, Existing Session mesajlarında kullanmak üzere her yön için olmak üzere iki etiket seti oluşturmak için kullanıyoruz. Son olarak, ek Existing Session mesajları için tek yönde yeni bir etiket seti oluşturmak amacıyla DH Ratchet sonrasında kullanıyoruz.

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

Bu, tagset tükenmeden önce, NextKey bloklarında yeni DH anahtarları değiştirildikten sonra kullanılır.

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### Mesaj Numaraları

Signal'deki gibi her mesaj için ratchet'lar. Session tag ratchet, simetrik anahtar ratchet ile senkronize edilir, ancak alıcı anahtar ratchet bellek tasarrufu için "geride kalabilir".

Transmitter gönderilen her mesaj için bir kez ratchet yapar. Hiçbir ek etiket saklanmamalıdır. Transmitter ayrıca mevcut zincirdeki mesajın mesaj numarası olan 'N' için bir sayaç tutmalıdır. 'N' değeri gönderilen mesaja dahil edilir. Message Number blok tanımına bakınız.

Alıcı, maksimum pencere boyutu kadar ileriye doğru ratchet yapmalı ve etiketleri oturum ile ilişkilendirilmiş bir "etiket seti"nde saklamalıdır. Alındıktan sonra, saklanan etiket atılabilir ve önceden alınmamış etiketler yoksa, pencere ilerletilebilir. Alıcı, her oturum etiketi ile ilişkilendirilmiş 'N' değerini tutmalı ve gönderilen mesajdaki sayının bu değerle eşleştiğini kontrol etmelidir. Message Number blok tanımına bakınız.

#### KDF

Bu, RATCHET_TAG() fonksiyonunun tanımıdır.

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### Örnek Uygulama

Signal'deki gibi her mesaj için ratchet'ler. Her simetrik anahtarın ilişkilendirilmiş bir mesaj numarası ve oturum etiketi vardır. Oturum anahtarı ratchet'i simetrik etiket ratchet'i ile senkronize edilir, ancak alıcı anahtarı ratchet'i bellek tasarrufu için "geride kalabilir".

Transmitter her iletilen mesaj için bir kez ratchet yapar. Ek anahtar saklanması gerekmez.

Alıcı bir oturum etiketi aldığında, simetrik anahtar ratchet'ini ilişkili anahtara kadar ilerletmemişse, ilişkili anahtara "yetişmek" zorundadır. Alıcı muhtemelen henüz alınmamış olan önceki etiketler için anahtarları önbellekte saklayacaktır. Alındıktan sonra, saklanan anahtar atılabilir ve önceden alınmamış etiket yoksa, pencere ilerletilebilir.

Verimlilik için, session tag ve simetrik anahtar ratchet'ları ayrıdır, böylece session tag ratchet'ı simetrik anahtar ratchet'ından önde gidebilir. Bu aynı zamanda ek güvenlik de sağlar, çünkü session tag'lar kablo üzerinden gönderilir.

#### KDF

Bu RATCHET_KEY() fonksiyonunun tanımıdır.

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet

Bu, ElGamal/AES+SessionTags spesifikasyonunda tanımlanan AES bölüm formatını değiştirir.

Bu, [NTCP2](/docs/specs/ntcp2/) spesifikasyonunda tanımlanan aynı blok formatını kullanır. Bireysel blok türleri farklı şekilde tanımlanır.

Uygulayıcıları kod paylaşmaya teşvik etmenin ayrıştırma sorunlarına yol açabileceğine dair endişeler bulunmaktadır. Uygulayıcılar kod paylaşmanın faydalarını ve risklerini dikkatle değerlendirmeli ve sıralama ile geçerli blok kurallarının iki bağlam için farklı olmasını sağlamalıdır.

### Payload Section Decrypted data

Şifreli uzunluk, verinin geri kalan kısmıdır. Şifresi çözülmüş uzunluk, şifreli uzunluktan 16 eksiktir. Tüm blok türleri desteklenir. Tipik içerikler aşağıdaki blokları içerir:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Şifrelenmiş çerçevede sıfır veya daha fazla blok bulunur. Her blok bir byte'lık tanımlayıcı, iki byte'lık uzunluk ve sıfır veya daha fazla byte veri içerir.

Genişletilebilirlik için, alıcılar bilinmeyen tip numaralarına sahip blokları görmezden GELMELİ ve bunları dolgu olarak ele almalıdır.

Şifrelenmiş veri maksimum 65535 bayttır ve bu 16 baytlık kimlik doğrulama başlığını içerir, dolayısıyla maksimum şifrelenmemiş veri 65519 bayttır.

(Poly1305 doğrulama etiketi gösterilmedi):

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

New Session mesajında, DateTime bloğu gereklidir ve ilk blok olmalıdır.

İzin verilen diğer bloklar:

- Garlic Clove (tip 11)
- Seçenekler (tip 5)
- Dolgu (tip 254)

New Session Reply mesajında hiçbir blok gerekli değildir.

İzin verilen diğer bloklar:

- Garlic Clove (tip 11)
- Seçenekler (tip 5)
- Dolgu (tip 254)

Başka hiçbir bloka izin verilmez. Padding, varsa, son blok olmalıdır.

Mevcut Oturum mesajında, hiçbir blok gerekli değildir ve aşağıdaki gereksinimler dışında sıra belirtilmemiştir:

Termination, eğer mevcutsa, Padding dışında son blok olmalıdır. Padding, eğer mevcutsa, son blok olmalıdır.

Tek bir çerçevede birden fazla Garlic Clove bloğu bulunabilir. Tek bir çerçevede en fazla iki Next Key bloğu bulunabilir. Tek bir çerçevede birden fazla Padding bloğuna izin verilmez. Diğer blok türleri muhtemelen tek bir çerçevede birden fazla bloğa sahip olmayacaktır, ancak bu yasaklanmamıştır.

### DateTime

Bir son kullanma tarihi. Yanıt önlemeye yardımcı olur. Bob, bu zaman damgasını kullanarak mesajın güncel olduğunu doğrulamalıdır. Bob, zaman geçerliyse, tekrar oynatma saldırılarını önlemek için bir Bloom filtresi veya başka bir mekanizma uygulamalıdır. Genellikle yalnızca New Session mesajlarında dahil edilir.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

[I2NP](/docs/specs/i2np/) spesifikasyonunda belirtildiği gibi tek bir şifresi çözülmüş Garlic Clove, kullanılmayan veya gereksiz alanları kaldırmak için yapılan değişikliklerle birlikte. Uyarı: Bu format ElGamal/AES için kullanılandan önemli ölçüde farklıdır. Her clove ayrı bir payload bloğudur. Garlic Clove'lar bloklar arasında veya ChaChaPoly frame'leri arasında parçalara ayrılamaz.

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Notlar:

- Uygulayıcılar, bir blok okunurken hatalı biçimlendirilmiş
  veya kötü amaçlı verilerin okumaların bir sonraki bloğa
  taşmasına neden olmayacağından emin olmalıdır.

- [I2NP](/docs/specs/i2np/) belirtiminde tanımlanan Clove Set formatı kullanılmaz.
  Her clove kendi bloğunda yer alır.

- I2NP mesaj başlığı 9 bayttır ve [NTCP2](/docs/specs/ntcp2/)'de kullanılanla aynı formata sahiptir.

- [I2NP](/docs/specs/i2np/) spesifikasyonundaki Garlic Message tanımından Certificate, Message ID ve Expiration dahil edilmemiştir.

- [I2NP](/docs/specs/i2np/)'deki Garlic Clove tanımından Certificate, Clove ID ve Expiration dahil edilmemiştir.

Gerekçe:

- Sertifikalar hiç kullanılmadı.
- Ayrı mesaj ID'si ve clove ID'leri hiç kullanılmadı.
- Ayrı son kullanma tarihleri hiç kullanılmadı.
- Eski Clove Set ve Clove formatlarına kıyasla genel tasarruf
  1 clove için yaklaşık 35 bayt, 2 clove için 54 bayt,
  ve 3 clove için 73 bayt'tır.
- Blok formatı genişletilebilir ve herhangi bir yeni alan
  yeni blok türleri olarak eklenebilir.

### Termination

Uygulama isteğe bağlıdır. Oturumu sonlandır. Bu, çerçevede son padding olmayan blok olmalıdır. Bu oturumda daha fazla mesaj gönderilmeyecektir.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) Simetrik Anahtar Ratchet

UYGULANMAMIŞ, ileri çalışma için. Güncellenmiş seçenekleri geçir. Seçenekler oturum için çeşitli parametreleri içerir. Daha fazla bilgi için aşağıdaki Session Tag Length Analysis bölümüne bakın.

Seçenekler bloğu değişken uzunlukta olabilir, çünkü more_options mevcut olabilir.

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW, gönderenin alıcıya yönelik olarak alıcının gelen etiket penceresi (maksimum ileri bakış) için önerisidir. RITW, gönderenin kullanmayı planladığı gelen etiket penceresi (maksimum ileri bakış) beyanıdır. Her iki taraf daha sonra ileri bakışı minimum, maksimum veya başka bir hesaplamaya dayalı olarak ayarlar veya düzenler.

Notlar:

- Varsayılan olmayan oturum etiketi uzunluğu desteğinin
  hiçbir zaman gerekli olmaması umulmaktadır.
- Etiket penceresi, Signal belgelerinde MAX_SKIP'tir.

Sorunlar:

- Seçenekler müzakeresi TBD.
- Varsayılanlar TBD.
- Dolgu ve gecikme seçenekleri NTCP2'den kopyalanmıştır,
  ancak bu seçenekler orada henüz tam olarak uygulanmamış veya incelenmemiştir.

### Message Numbers

Uygulama isteğe bağlıdır. Önceki etiket kümesindeki uzunluk (gönderilen mesaj sayısı) (PN). Alıcı, önceki etiket kümesinden PN'den yüksek etiketleri hemen silebilir. Alıcı, önceki etiket kümesinden PN'den küçük veya eşit etiketleri kısa bir süre sonra (örneğin 2 dakika) silebilir.

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
Notlar:

- Maksimum PN 65535'tir.
- PN tanımı Signal tanımına eşittir, eksi bir.
  Bu Signal'in yaptığına benzer, ancak Signal'de PN ve N başlıkta bulunur.
  Burada, şifrelenmiş mesaj gövdesinde yer alırlar.
- Bu bloğu tag set 0'da göndermeyin, çünkü önceki tag set yoktu.

### 5) Yük Verisi

Bir sonraki DH ratchet anahtarı payload içindedir ve isteğe bağlıdır. Her seferinde ratchet yapmayız. (Bu Signal'den farklıdır, orada header içindedir ve her seferinde gönderilir)

İlk ratchet için, Key ID = 0.

NS veya NSR'da izin verilmez. Sadece Mevcut Oturum mesajlarında dahil edilir.

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
Notlar:

- Key ID, o etiket seti için kullanılan yerel anahtar için artan bir sayaçtır, 0'dan başlar.
- ID, anahtar değişmedikçe değişmemelidir.
- Kesinlikle gerekli olmayabilir, ancak hata ayıklama için yararlıdır.
  Signal bir key ID kullanmaz.
- Maksimum Key ID 32767'dir.
- Her iki yöndeki etiket setlerinin aynı anda ratcheting yaptığı nadir durumda, bir frame iki Next Key bloğu içerecektir, biri forward anahtarı için, diğeri reverse anahtarı için.
- Anahtar ve etiket seti ID numaraları ardışık olmalıdır.
- Ayrıntılar için yukarıdaki DH Ratchet bölümüne bakın.

### Payload Bölümü Şifresi çözülmüş veri

Bu yalnızca bir ack request bloğu alınmışsa gönderilir. Birden fazla mesajı ack'lemek için birden fazla ack mevcut olabilir.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
Notlar:

- Etiket kümesi ID'si ve N, onaylanan mesajı benzersiz şekilde tanımlar.
- Her yönde bir oturum için kullanılan ilk etiket kümelerinde, etiket kümesi ID'si 0'dır.
- Hiçbir NextKey bloğu gönderilmemiştir, bu nedenle anahtar ID'leri yoktur.
- NextKey değişimlerinden sonra kullanılan tüm etiket kümeleri için, etiket kümesi numarası (1 + Alice'in anahtar ID'si + Bob'un anahtar ID'si)'dir.

### Şifrelenmemiş veri

Bir in-band ack talep et. Garlic Clove içindeki out-of-band DeliveryStatus Message'ı değiştirmek için.

Açık bir ack talep edilirse, mevcut tagset ID'si ve mesaj numarası (N) bir ack bloğunda döndürülür.

NS veya NSR'de izin verilmez. Yalnızca Mevcut Oturum mesajlarında dahil edilir.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Blok Sıralama Kuralları

Tüm padding AEAD çerçeveleri içindedir. TODO AEAD içindeki padding kabaca müzakere edilen parametrelere uymalıdır. TODO Alice istediği tx/rx min/max parametrelerini NS mesajında gönderdi. TODO Bob istediği tx/rx min/max parametrelerini NSR mesajında gönderdi. Güncellenmiş seçenekler veri aşaması sırasında gönderilebilir. Yukarıdaki seçenekler bloğu bilgilerine bakın.

Mevcut ise, bu frame'deki son blok olmalıdır.

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
Notlar:

- Tamamen sıfır dolgulama uygun, şifrelenecek olduğu için.
- Dolgu stratejileri henüz belirlenmedi.
- Sadece dolgu içeren çerçevelere izin verilir.
- Dolgu varsayılanı 0-15 bayttır.
- Dolgu parametresi müzakeresi için seçenekler bloğuna bakın
- Minimum/maksimum dolgu parametreleri için seçenekler bloğuna bakın
- Router'ın müzakere edilen dolgu ihlali durumundaki tepkisi implementasyona bağlıdır.

### Tarih Saat

Uygulamalar, ileriye dönük uyumluluk için bilinmeyen blok türlerini görmezden gelmelidir.

### Garlic Clove

- Dolgu uzunluğu ya mesaj bazında karar verilmeli ve uzunluk dağılımı tahminleri yapılmalı, ya da rastgele gecikmeler eklenmelidir. Bu karşı önlemler DPI'ye direnç göstermek için dahil edilmelidir, aksi takdirde mesaj boyutları I2P trafiğinin taşıma protokolü tarafından taşındığını açığa çıkaracaktır. Kesin dolgu şeması gelecekteki çalışmaların bir alanıdır, Ek A bu konu hakkında daha fazla bilgi sağlar.

## Typical Usage Patterns

### Sonlandırma

Bu en tipik kullanım durumudur ve HTTP olmayan çoğu akış kullanım durumu da bu kullanım durumu ile aynı olacaktır. Küçük bir başlangıç mesajı gönderilir, bir yanıt gelir ve her iki yönde de ek mesajlar gönderilir.

Bir HTTP GET genellikle tek bir I2NP mesajına sığar. Alice, bir yanıt leaseSet'i paketleyerek tek yeni Session mesajıyla küçük bir istek gönderir. Alice yeni anahtara anında ratchet içerir. Hedefle bağlamak için imza içerir. Onay talep edilmez.

Bob hemen ratchet yapar.

Alice hemen ratchet yapar.

Bu oturumlarla devam eder.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### Seçenekler

Alice'in üç seçeneği var:

1) Yalnızca ilk mesajı gönder (pencere boyutu = 1), HTTP GET'te olduğu gibi. Önerilmez.

2) Streaming pencere boyutuna kadar gönder, ancak aynı Elligator2-kodlanmış açık metin public key kullanarak. Tüm mesajlar aynı sonraki public key'i (ratchet) içerir. Bu, OBGW/IBEP tarafından görülebilir olacaktır çünkü hepsi aynı açık metinle başlar. İşlemler 1)'deki gibi devam eder. Önerilmez.

3) Önerilen uygulama. Streaming penceresine kadar gönder, ancak her biri için farklı bir Elligator2-kodlanmış açık metin public key (oturum) kullan. Tüm mesajlar aynı next public key (ratchet) içerir. Bu OBGW/IBEP tarafından görülemeyecek çünkü hepsi farklı açık metinle başlar. Bob hepsinin aynı next public key içerdiğini tanımalı ve hepsine aynı ratchet ile yanıt vermeli. Alice bu next public key'i kullanır ve devam eder.

Seçenek 3 mesaj akışı:

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### Mesaj Numaraları

Tek bir yanıt beklenen tek bir mesaj. Ek mesajlar veya yanıtlar gönderilebilir.

HTTP GET'e benzer, ancak oturum etiketi pencere boyutu ve yaşam süresi için daha küçük seçeneklerle. Belki ratchet talep etmeyin.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### Sonraki DH Ratchet Genel Anahtarı

Yanıt beklenmeden birden fazla anonim mesaj.

Bu senaryoda, Alice bir oturum talep eder, ancak bağlama olmadan. Yeni oturum mesajı gönderilir. Hiçbir yanıt LS paketlenmez. Bir yanıt DSM paketlenir (bu, paketlenmiş DSM'ler gerektiren tek kullanım durumudur). Hiçbir sonraki anahtar dahil edilmez. Hiçbir yanıt veya ratchet talep edilmez. Hiçbir ratchet gönderilmez. Seçenekler, oturum etiketleri penceresini sıfıra ayarlar.

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### Onay

Yanıt beklenmeden gönderilen tek bir anonim mesaj.

Tek seferlik mesaj gönderilir. Hiçbir yanıt LS veya DSM paketlenmez. Sonraki anahtar dahil edilmez. Hiçbir yanıt veya ratchet istenmez. Hiçbir ratchet gönderilmez. Seçenekler oturum etiketleri penceresini sıfıra ayarlar.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Onay İsteği

Uzun yaşamlı oturumlar, o andan itibaren forward secrecy'yi korumak için herhangi bir zamanda ratchet yapabilir veya ratchet talep edebilir. Oturumlar, oturum başına gönderilen mesaj sınırına (65535) yaklaştıkça ratchet yapmalıdır.

## Implementation Considerations

### Dolgu

Mevcut ElGamal/AES+SessionTag protokolünde olduğu gibi, uygulamalar session tag depolamasını sınırlamalı ve bellek tüketme saldırılarına karşı korunmalıdır.

Önerilen bazı stratejiler şunlardır:

- Saklanan oturum etiketlerinin sayısında katı limit
- Bellek baskısı altındayken boştaki gelen oturumların agresif şekilde sonlandırılması
- Tek bir uzak hedef destinasyona bağlı gelen oturum sayısında limit
- Bellek baskısı altındayken oturum etiketi penceresinin adaptif olarak azaltılması ve eski kullanılmayan etiketlerin silinmesi
- Bellek baskısı altındayken istek geldiğinde ratchet işlemini reddetme

### Diğer blok türleri

Önerilen parametreler ve zaman aşımları:

- NSR tagset boyutu: 12 tsmin ve tsmax
- ES tagset 0 boyutu: tsmin 24, tsmax 160
- ES tagset (1+) boyutu: 160 tsmin ve tsmax
- NSR tagset zaman aşımı: alıcı için 3 dakika
- ES tagset zaman aşımı: gönderici için 8 dakika, alıcı için 10 dakika
- Önceki ES tagset'i kaldırma süresi: 3 dakika sonra
- Tag N için tagset önceden bakma: min(tsmax, tsmin + N/4)
- Tag N arkasında tagset kırpma: min(tsmax, tsmin + N/4) / 2
- Sonraki anahtarı gönderme tag'i: TBD
- Tagset yaşam süresinden sonra sonraki anahtarı gönderme: TBD
- NS alındıktan sonra oturumu değiştirme süresi: 3 dakika
- Maksimum saat sapması: -5 dakika ile +2 dakika arası
- NS tekrar filtresi süresi: 5 dakika
- Padding boyutu: 0-15 bayt (diğer stratejiler TBD)

### Gelecekteki çalışmalar

Gelen mesajları sınıflandırmak için öneriler aşağıda verilmiştir.

### X25519 Only

Bu protokol ile yalnızca kullanılan bir tunnel üzerinde, şu anda ElGamal/AES+SessionTags ile yapıldığı gibi kimlik doğrulama yapın:

Öncelikle, başlangıç verisini bir oturum etiketi olarak değerlendirin ve oturum etiketini arayın. Bulunursa, o oturum etiketiyle ilişkili saklanan veriyi kullanarak şifre çözme işlemini gerçekleştirin.

Bulunamazsa, başlangıç verisini bir DH public key ve nonce olarak ele alın. Bir DH işlemi ve belirtilen KDF gerçekleştirin, ve kalan veriyi şifresini çözmeyi deneyin.

### HTTP GET

Bu protokolü ve ElGamal/AES+SessionTags protokolünü destekleyen bir tunnel üzerinde, gelen mesajları şu şekilde sınıflandırın:

ElGamal/AES+SessionTags spesifikasyonundaki bir kusur nedeniyle, AES bloğu rastgele mod-16 olmayan bir uzunluğa doldurulmaz. Bu nedenle, Mevcut Oturum mesajlarının uzunluğunun mod 16'sı her zaman 0'dır ve Yeni Oturum mesajlarının uzunluğunun mod 16'sı her zaman 2'dir (ElGamal bloğu 514 bayt uzunluğunda olduğu için).

Uzunluk mod 16 değeri 0 veya 2 değilse, başlangıç verisini bir session tag olarak değerlendirin ve session tag'i arayın. Bulunursa, o session tag ile ilişkili saklanan veriyi kullanarak şifresini çözün.

Bulunamazsa ve uzunluk mod 16'sı 0 veya 2 değilse, başlangıç verilerini bir DH public key ve nonce olarak değerlendirin. Bir DH işlemi ve belirtilen KDF gerçekleştirin, ve kalan veriyi şifrelemeden çıkarmaya çalışın. (göreceli trafik karışımına ve X25519 ile ElGamal DH işlemlerinin göreceli maliyetlerine dayalı olarak, bu adım bunun yerine en son yapılabilir)

Aksi takdirde, uzunluk mod 16 değeri 0 ise, başlangıç verisini bir ElGamal/AES session tag olarak işle ve session tag'i ara. Bulunursa, o session tag ile ilişkilendirilen saklanan veriyi kullanarak şifrele.

Bulunamazsa ve veri en az 642 (514 + 128) bayt uzunluğundaysa ve uzunluğun 16'ya bölümünden kalan 2 ise, başlangıç verisini ElGamal bloğu olarak değerlendir. Kalan veriyi şifrelerini çözmeye çalış.

ElGamal/AES+SessionTag spesifikasyonunun mod-16 olmayan padding'e izin verecek şekilde güncellenmesi durumunda, işlerin farklı şekilde yapılması gerekecektir.

### HTTP POST

İlk uygulamalar, üst katmanlarda çift yönlü trafiğe dayanır. Yani, uygulamalar ters yöndeki trafiğin yakında iletileceğini varsayar ve bu da ECIES katmanında gerekli herhangi bir yanıtı zorlar.

Ancak, belirli trafik tek yönlü veya çok düşük bant genişlikli olabilir, öyle ki zamanında yanıt oluşturacak üst katman trafiği bulunmaz.

NS ve NSR mesajlarının alınması bir yanıt gerektirir; ACK Request ve Next Key bloklarının alınması da bir yanıt gerektirir.

Gelişmiş bir uygulama, yanıt gerektiren bu mesajlardan biri alındığında bir zamanlayıcı başlatabilir ve kısa bir süre içinde (örneğin 1 saniye) ters yönde trafik gönderilmezse ECIES katmanında "boş" (Garlic Clove bloğu olmayan) bir yanıt oluşturabilir.

NS ve NSR mesajlarına verilen yanıtlar için daha da kısa bir zaman aşımı süresi uygun olabilir, bu sayede trafik mümkün olan en kısa sürede verimli ES mesajlarına kaydırılabilir.

## Analysis

### Yanıtlanabilir Datagram

Her yönde ilk iki mesaj için mesaj ek yükü aşağıdaki gibidir. Bu, ACK'den önce her yönde yalnızca bir mesaj olduğunu veya herhangi bir ek mesajın spekülatif olarak Mevcut Oturum mesajları olarak gönderildiğini varsayar. Teslim edilen oturum etiketlerinin spekülatif ACK'leri yoksa, eski protokolün ek yükü çok daha yüksektir.

Yeni protokolün analizi için herhangi bir padding varsayılmaz. Paketlenmiş leaseset varsayılmaz.

### Çoklu Ham Veri Paketleri

Yeni oturum mesajı, her yönde aynı:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Mevcut oturum mesajları, her yönde aynı:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Tek Ham Datagram

Alice-to-Bob Yeni Oturum mesajı:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Bob'dan Alice'e Yeni Oturum Yanıt mesajı:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Mevcut oturum mesajları, her yönde aynı:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Uzun Süreli Oturumlar

Toplam dört mesaj (her yönde ikişer):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Yalnızca handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Uzun vadeli toplam (el sıkışmalar hariç):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO bu bölümü öneri kararlı hale geldikten sonra güncelleyin.

Her bir tarafın New Session ve New Session Reply mesajlarını değiş tokuş etmesi için aşağıdaki kriptografik işlemler gereklidir:

- HMAC-SHA256: HKDF başına 3, toplam TBD
- ChaChaPoly: her biri için 2
- X25519 anahtar üretimi: 2 Alice, 1 Bob
- X25519 DH: her biri için 3
- İmza doğrulama: 1 (Bob)

Alice her bound-session başına (minimum) 5 ECDH hesaplar, Bob'a gönderdiği her NS mesajı için 2 ve Bob'un her NSR mesajı için 3.

Bob ayrıca bağlı-oturum başına 6 ECDH hesaplar, Alice'in NS mesajlarının her biri için 3 ve kendi NSR mesajlarının her biri için 3.

Her bir taraf tarafından her Mevcut Oturum mesajı için aşağıdaki kriptografik işlemler gereklidir:

- HKDF: 2
- ChaChaPoly: 1

### Savunma

Mevcut oturum etiketi uzunluğu 32 bayttır. Bu uzunluk için henüz herhangi bir gerekçe bulamadık, ancak arşivleri araştırmaya devam ediyoruz. Yukarıdaki öneri yeni etiket uzunluğunu 8 bayt olarak tanımlar. 8 baytlık bir etiketi gerekçelendiren analiz şu şekildedir:

Session tag ratchet'ının rastgele, düzgün dağıtılmış etiketler ürettiği varsayılır. Belirli bir session tag uzunluğu için kriptografik bir neden yoktur. Session tag ratchet, simetrik anahtar ratchet'ı ile senkronize edilir, ancak ondan bağımsız bir çıktı üretir. İki ratchet'ın çıktıları farklı uzunluklarda olabilir.

Bu nedenle, tek endişe session tag çakışmasıdır. Uygulamaların her iki session ile şifre çözmeyi deneyerek çakışmaları ele almaya çalışmayacağı varsayılmaktadır; uygulamalar tag'i önceki veya yeni session'dan biriyle ilişkilendirecek ve diğer session'da bu tag ile alınan herhangi bir mesaj, şifre çözme işlemi başarısız olduktan sonra atılacaktır.

Amaç, çakışma riskini minimize edecek kadar büyük, ancak bellek kullanımını minimize edecek kadar küçük bir oturum etiketi uzunluğu seçmektir.

Bu, uygulamaların bellek tükenme saldırılarını önlemek için session tag depolamasını sınırladığını varsayar. Bu aynı zamanda bir saldırganın çakışmalar yaratabilme şansını büyük ölçüde azaltacaktır. Aşağıdaki Uygulama Hususları bölümüne bakın.

En kötü durum için, saniyede 64 yeni gelen oturum bulunan yoğun bir sunucu varsayın. 15 dakikalık gelen oturum tag ömrü varsayın (şu anki ile aynı, muhtemelen azaltılmalı). 32'lik gelen oturum tag penceresi varsayın. 64 * 15 * 60 * 32 = 1,843,200 tag Mevcut Java I2P maksimum gelen tag sayısı 750,000'dir ve bildiğimiz kadarıyla hiç bu sayıya ulaşılmamıştır.

Milyonda 1 (1e-6) oranında session tag çarpışması hedefi muhtemelen yeterlidir. Tıkanıklık nedeniyle yol boyunca bir mesajın düşürülme olasılığı bundan çok daha yüksektir.

Ref: https://en.wikipedia.org/wiki/Birthday_paradox Olasılık tablosu bölümü.

32 baytlık session tag'ler (256 bit) ile session tag alanı 1,2e77'dir. 1e-18 olasılıkla çarpışma olasılığı 4,8e29 giriş gerektirir. 1e-6 olasılıkla çarpışma olasılığı 4,8e35 giriş gerektirir. Her biri 32 bayt olan 1,8 milyon tag toplam yaklaşık 59 MB'dır.

16 bayt session tag'leri (128 bit) ile session tag alanı 3.4e38'dir. 1e-18 olasılıkla çakışma olasılığı 2.6e10 girdi gerektirir. 1e-6 olasılıkla çakışma olasılığı 2.6e16 girdi gerektirir. Her biri 16 bayt olan 1.8 milyon tag toplamda yaklaşık 30 MB'dir.

8 baytlık session tag'leri (64 bit) ile session tag alanı 1.8e19'dur. 1e-18 olasılıkla bir çakışma olasılığı 6.1 girdi gerektirir. 1e-6 olasılıkla bir çakışma olasılığı 6.1e6 (6,100,000) girdi gerektirir. Her biri 8 bayt olan 1.8 milyon tag toplam yaklaşık 15 MB'dir.

6,1 milyon aktif etiket, en kötü durum tahminimiz olan 1,8 milyon etiketin 3 katından fazlasıdır. Bu nedenle çarpışma olasılığı milyonda birden az olacaktır. Dolayısıyla 8 baytlık session tag'lerinin yeterli olduğu sonucuna varıyoruz. Bu, transmit tag'lerinin saklanmaması nedeniyle elde edilen 2 kat azalmaya ek olarak 4 kat depolama alanı azalması sağlar. Böylece ElGamal/AES+SessionTags'e kıyasla session tag bellek kullanımında 8 kat azalma elde edeceğiz.

Bu varsayımların yanlış olması durumunda esnekliği korumak için, seçeneklere bir oturum etiketi uzunluk alanı ekleyeceğiz, böylece varsayılan uzunluk oturum bazında geçersiz kılınabilir. Kesinlikle gerekli olmadıkça dinamik etiket uzunluğu müzakeresi uygulamayı beklemiyoruz.

Uygulamalar, en azından oturum etiketi çakışmalarını tanımalı, bunları zarif bir şekilde ele almalı ve çakışma sayısını günlüğe kaydetmeli veya saymalıdır. Hala son derece olası olmasa da, ElGamal/AES+SessionTags için olduklarından çok daha olası olacaklar ve gerçekten de gerçekleşebilirler.

### Parametreler

Saniye başına iki katı oturum (128) ve iki katı etiket penceresi (64) kullandığımızda, 4 kat etiketimiz (7,4 milyon) oluyor. Milyonda bir çarpışma şansı için maksimum 6,1 milyon etikettir. 12 bayt (hatta 10 bayt) etiketler büyük bir güvenlik payı eklerdi.

Ancak, milyonda bir çarpışma şansı iyi bir hedef midir? Yol boyunca düşürülme şansından çok daha büyük olması pek faydalı değildir. Java'nın DecayingBloomFilter'ı için false-positive hedefi kabaca 10.000'de 1'dir, ancak 1000'de 1 bile ciddi bir endişe kaynağı değildir. Hedefi 10.000'de 1'e düşürerek, 8 byte tag'lerle yeterli marj elde edilir.

### Sınıflandırma

Gönderen, tag'leri ve anahtarları anlık olarak oluşturur, bu nedenle depolama yoktur. Bu, ElGamal/AES'e kıyasla genel depolama gereksinimlerini yarıya indirir. ECIES tag'leri ElGamal/AES için 32 byte yerine 8 byte'tır. Bu, genel depolama gereksinimlerini 4 kat daha fazla azaltır. Tag başına oturum anahtarları, makul kayıp oranları için minimal olan "boşluklar" dışında alıcıda depolanmaz.

Etiket süre dolum zamanındaki %33'lük azalma, kısa oturum süreleri varsayılarak, başka bir %33'lük tasarruf sağlar.

Bu nedenle, ElGamal/AES'e karşı toplam alan tasarrufu 10,7 kat veya %92'dir.

## Related Changes

### Yalnızca X25519

ECIES Hedeflerinden Veritabanı Sorguları: Bkz. [Teklif 154](/proposals/154-ecies-lookups), şimdi 0.9.46 sürümü için [I2NP](/docs/specs/i2np/) içine dahil edilmiştir.

Bu öneri, X25519 public key'ini leaseset ile birlikte yayınlamak için LS2 desteği gerektirmektedir. [I2NP](/docs/specs/i2np/)'deki LS2 spesifikasyonlarında herhangi bir değişiklik yapılması gerekmemektedir. Tüm destek, 0.9.38 sürümünde uygulanan [Proposal 123](/proposals/123-new-netdb-entries)'te tasarlanmış, belirtilmiş ve uygulanmıştır.

### X25519 ElGamal/AES+SessionTags ile Paylaşımlı

Hiçbiri. Bu öneri LS2 desteği gerektirir ve etkinleştirilmek için I2CP seçeneklerinde bir özelliğin ayarlanmasını gerektirir. [I2CP](/docs/specs/i2cp/) spesifikasyonlarında herhangi bir değişiklik gerekmemektedir. Tüm destek, 0.9.38 sürümünde uygulanan [Öneri 123](/proposals/123-new-netdb-entries)'te tasarlanmış, belirtilmiş ve uygulanmıştır.

ECIES'i etkinleştirmek için gereken seçenek, I2CP, BOB, SAM veya i2ptunnel için tek bir I2CP özelliğidir.

Tipik değerler yalnızca ECIES için i2cp.leaseSetEncType=4 veya ECIES ve ElGamal çift anahtarları için i2cp.leaseSetEncType=4,0 şeklindedir.

### Protokol Katmanı Yanıtları

Bu bölüm [Proposal 123](/proposals/123-new-netdb-entries) sayfasından kopyalanmıştır.

SessionConfig Eşlemesindeki Seçenek:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Bu öneri 0.9.38 sürümünden itibaren desteklenen LS2 gerektirir. [I2CP](/docs/specs/i2cp/) spesifikasyonlarında herhangi bir değişiklik gerekmez. Tüm destek 0.9.38'de uygulanan [Proposal 123](/proposals/123-new-netdb-entries)'te tasarlandı, belirtildi ve uygulandı.

### Ek Yük

Çift anahtarları olan LS2'yi destekleyen herhangi bir router (0.9.38 veya üzeri) çift anahtarlı destinasyonlara bağlantıyı desteklemelidir.

Yalnızca ECIES hedefler, şifreli arama yanıtları alabilmek için floodfill'lerin çoğunluğunun 0.9.46 sürümüne güncellenmesini gerektirir. Bkz. [Teklif 154](/proposals/154-ecies-lookups).

Yalnızca ECIES destinasyonlar, yalnızca ECIES olan veya çift anahtarlı diğer destinasyonlarla bağlantı kurabilir.
