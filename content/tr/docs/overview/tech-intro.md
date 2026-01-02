---
title: "I2P: Anonim iletişim için ölçeklenebilir bir çerçeve"
description: "I2P mimarisi ve işleyişine teknik giriş"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Giriş

I2P, ölçeklenebilir, kendi kendini organize eden, dayanıklı bir paket anahtarlamalı anonim ağ katmanıdır ve bu katman üzerinde anonimlik veya güvenlik odaklı herhangi bir sayıda farklı uygulama çalışabilir. Bu uygulamaların her biri, serbest rota mixnet'in (karıştırma ağı) doğru uygulanması konusunda endişelenmeden kendi anonimlik, gecikme ve aktarım hızı dengesini kurabilir; böylece faaliyetlerini I2P üzerinde zaten çalışan daha geniş kullanıcı anonimlik kümesiyle harmanlamalarına olanak tanır.

Halihazırda mevcut uygulamalar, tipik İnternet etkinliklerinin tüm yelpazesini sağlar — **anonim** web taraması, web barındırma, sohbet, dosya paylaşımı, e-posta, blog yazarlığı ve içerik sendikasyonunun yanı sıra geliştirme aşamasında olan diğer birkaç uygulama.

- **Web tarayıcı kullanımı:** proxy destekleyen herhangi bir mevcut tarayıcı kullanarak  
- **Sohbet:** IRC ve diğer protokoller  
- **Dosya paylaşımı:** [I2PSnark](#i2psnark) ve diğer uygulamalar  
- **E-posta:** [Susimail](#i2pmail) ve diğer uygulamalar  
- **Blog:** herhangi bir yerel web sunucusu veya mevcut eklentiler kullanarak

[Freenet](/docs/overview/comparison#freenet) veya [GNUnet](https://www.gnunet.org/) gibi içerik dağıtım ağlarında barındırılan web sitelerinin aksine, I2P üzerinde barındırılan hizmetler tamamen etkileşimlidir — geleneksel web tarzı arama motorları, bülten panoları, yorum yapabileceğiniz bloglar, veritabanı destekli siteler ve Freenet gibi statik sistemleri yerel olarak kurmaya gerek kalmadan sorgulayabileceğiniz köprüler bulunur.

Tüm bu anonimlik özellikli uygulamalarla birlikte, I2P **mesaj odaklı ara katman yazılımı** olarak işlev görür — uygulamalar, kriptografik bir tanımlayıcıya (bir "destination") gönderilecek veriyi belirtir ve I2P bunun güvenli ve anonim bir şekilde ulaşmasını sağlar. I2P ayrıca, I2P'nin anonim en iyi çaba mesajlarının güvenilir, sıralı akışlar olarak aktarılmasına olanak tanıyan basit bir [streaming kütüphanesi](#streaming) içerir ve ağın yüksek bant genişliği-gecikme çarpımına göre ayarlanmış TCP tabanlı tıkanıklık kontrolü sunar.

Basit SOCKS proxy'leri mevcut uygulamaları bağlamak için geliştirilmiş olsa da, çoğu uygulama anonim bir bağlamda hassas bilgileri sızdırdığı için değerleri sınırlıdır. En güvenli yaklaşım, uygulamayı I2P'nin API'lerini doğrudan kullanacak şekilde **denetlemek ve uyarlamaktır**.

I2P bir araştırma projesi değildir — ne akademik, ne ticari, ne de devlet destekli — kullanılabilir anonimlik sağlamayı hedefleyen bir mühendislik çabasıdır. 2003'ün başından beri dünya çapında dağıtık bir katkıda bulunanlar grubu tarafından sürekli olarak geliştirilmektedir. Tüm I2P çalışmaları [resmi web sitesinde](https://geti2p.net/) **açık kaynak** olup, öncelikli olarak kamu malı olarak yayınlanmakta, bazı bileşenler ise izin verici BSD-tarzı lisanslar altındadır. [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) ve [I2PSnark](#i2psnark) gibi çeşitli GPL lisanslı istemci uygulamaları mevcuttur. Finansman yalnızca kullanıcı bağışlarından gelmektedir.

---

## İşlem

### Overview

I2P, router'lar (ağa katılan düğümler) ile destination'lar (uygulamalar için anonim uç noktalar) arasında net bir ayrım yapar. I2P'nin kendisini çalıştırmak gizli değildir; gizlenen şey kullanıcının **ne** yaptığı ve destination'larının hangi router'ı kullandığıdır. Son kullanıcılar genellikle birkaç destination çalıştırır (örneğin, biri web taraması için, diğeri barındırma için, bir diğeri IRC için).

I2P'de temel bir kavram **tunnel** (tünel) — bir dizi router üzerinden geçen tek yönlü şifreli bir yoldur. Her router yalnızca bir katmanı çözer ve yalnızca bir sonraki adımı öğrenir. Tunneller her 10 dakikada bir sona erer ve yeniden oluşturulması gerekir.

![Gelen ve giden tünel şeması](/images/tunnels.png)   *Şekil 1: İki tür tünel vardır — gelen (inbound) ve giden (outbound).*

- **Giden tüneller** (Outbound tunnels), mesajları oluşturucudan uzağa gönderir.  
- **Gelen tüneller** (Inbound tunnels), mesajları oluşturucuya geri getirir.

Bunları birleştirmek iki yönlü iletişim sağlar. Örneğin, "Alice" giden bir tunnel kullanarak "Bob'un" gelen tunnel'ına gönderim yapar. Alice mesajını Bob'un gelen gateway'ine yönlendirme talimatlarıyla şifreler.

Diğer önemli bir kavram ise router'lar ve hedefler hakkında üst verileri dağıtan **network database** veya **netDb**'dir:

- **RouterInfo:** Yönlendirici iletişim ve anahtar materyalini içerir.  
- **LeaseSet:** Bir hedefe ulaşmak için gereken bilgileri içerir (tunnel ağ geçitleri, son kullanma süreleri, şifreleme anahtarları).

Router'lar RouterInfo bilgilerini doğrudan netDb'ye yayınlar; LeaseSet'ler ise anonimlik için giden tüneller üzerinden gönderilir.

Tüneller oluşturmak için Alice, eş seçmek amacıyla netDb'yi RouterInfo girişleri için sorgular ve tünel tamamlanana kadar şifrelenmiş tünel oluşturma mesajlarını atlama-atlama (hop-by-hop) gönderir.

![Router bilgileri tünel oluşturmak için kullanılır](/images/netdb_get_routerinfo_2.png)   *Şekil 2: Router bilgileri tünel oluşturmak için kullanılır.*

Bob'a göndermek için, Alice Bob'un LeaseSet'ini arar ve verilerini Bob'un gelen tünel ağ geçidine yönlendirmek için kendi giden tünellerinden birini kullanır.

![LeaseSets gelen ve giden tünelleri bağlar](/images/netdb_get_leaseset.png)   *Şekil 3: LeaseSets giden ve gelen tünelleri bağlar.*

I2P mesaj tabanlı olduğu için, mesajları giden uç nokta veya gelen ağ geçidinden bile korumak için **uçtan uca garlic encryption** ekler. Bir garlic mesajı, meta verileri gizlemek ve anonimliği artırmak için birden fazla şifrelenmiş "clove" (mesaj) içerir.

Uygulamalar mesaj arayüzünü doğrudan kullanabilir veya güvenilir bağlantılar için [streaming kütüphanesine](#streaming) güvenebilir.

---

### Tunnels

Hem gelen hem de giden tüneller katmanlı şifreleme kullanır, ancak yapıları farklıdır:

- **Gelen tünellerde**, oluşturucu (uç nokta) tüm katmanların şifresini çözer.
- **Giden tünellerde**, oluşturucu (ağ geçidi) uç noktada netliği sağlamak için katmanların şifresini önceden çözer.

I2P, eşleri doğrudan yoklama yapmadan gecikme ve güvenilirlik gibi dolaylı metrikler aracılığıyla profiller. Bu profillere dayanarak, eşler dinamik olarak dört katmana gruplandırılır:

1. Hızlı ve yüksek kapasite  
2. Yüksek kapasite  
3. Başarısız olmayan  
4. Başarısız olan

Tunnel eş seçimi genellikle yüksek kapasiteli eşleri tercih eder, anonimlik ve performansı dengelemek için rastgele seçilir ve predecessor saldırılarını ve netDb toplamasını azaltmak için ek XOR tabanlı sıralama stratejileri kullanır.

Daha detaylı bilgi için [Tunnel Specification](/docs/specs/implementation) bölümüne bakınız.

---

### Genel Bakış

**Floodfill** dağıtılmış hash tablosuna (DHT) katılan router'lar LeaseSet aramalarını depolar ve yanıtlar. DHT, [Kademlia](https://en.wikipedia.org/wiki/Kademlia)'nın bir varyantını kullanır. Floodfill router'lar, yeterli kapasiteye ve kararlılığa sahiplerse otomatik olarak seçilir veya manuel olarak yapılandırılabilir.

- **RouterInfo:** Bir router'ın yeteneklerini ve aktarım yöntemlerini tanımlar.  
- **LeaseSet:** Bir hedefin tunnel'larını ve şifreleme anahtarlarını tanımlar.

netDb'deki tüm veriler yayıncı tarafından imzalanır ve tekrar oynatma ya da bayat girdi saldırılarını önlemek için zaman damgası eklenir. Zamanlama senkronizasyonu SNTP ve aktarım katmanı sapma tespiti aracılığıyla sağlanır.

#### Additional concepts

- **Yayınlanmamış ve şifrelenmiş LeaseSet'ler:**  
  Bir hedef (destination), LeaseSet'ini yayınlamayarak ve yalnızca güvenilir eşlerle paylaşarak gizli kalabilir. Erişim için uygun şifre çözme anahtarı gereklidir.

- **Bootstrapping (reseeding):**  
  Ağa katılmak için, yeni bir router güvenilir HTTPS reseed sunucularından imzalanmış RouterInfo dosyalarını alır.

- **Arama ölçeklenebilirliği:**  
  I2P, DHT ölçeklenebilirliğini ve güvenliğini artırmak için özyinelemeli değil, **yinelemeli** aramalar kullanır.

---

### Tüneller

Modern I2P iletişimi iki tamamen şifrelenmiş aktarım kullanır:

- **[NTCP2](/docs/specs/ntcp2):** Şifrelenmiş TCP tabanlı protokol  
- **[SSU2](/docs/specs/ssu2):** Şifrelenmiş UDP tabanlı protokol

Her ikisi de modern [Noise Protocol Framework](https://noiseprotocol.org/) üzerine kurulmuştur ve güçlü kimlik doğrulama ile trafik parmak izi almaya karşı direnç sağlar. Eski NTCP ve SSU protokollerinin yerini almışlardır (2023'ten beri tamamen kullanımdan kaldırılmıştır).

**NTCP2**, TCP üzerinden şifrelenmiş ve verimli akış sunar.

**SSU2**, UDP tabanlı güvenilirlik, NAT geçişi ve isteğe bağlı hole punching sağlar. SSU2 kavramsal olarak WireGuard veya QUIC'e benzer şekilde güvenilirlik ve anonimlik arasında denge kurar.

Router'lar hem IPv4 hem de IPv6'yı destekleyebilir ve transport adreslerini ve maliyetlerini netDb'de yayınlar. Bir bağlantının transport'u, koşulları ve mevcut bağlantıları optimize eden bir **ihale sistemi** tarafından dinamik olarak seçilir.

---

### Ağ Veritabanı (netDb)

I2P tüm bileşenler için katmanlı şifreleme kullanır: taşımalar, tüneller, garlic mesajları ve network database.

Mevcut temel işlevler şunları içerir:

- Anahtar değişimi için X25519  
- İmzalar için EdDSA (Ed25519)  
- Kimlik doğrulamalı şifreleme için ChaCha20-Poly1305  
- Hash işlemleri için SHA-256  
- Tunnel katmanı şifrelemesi için AES256

Eski algoritmalar (ElGamal, DSA-SHA1, ECDSA) geriye dönük uyumluluk için korunmuştur.

I2P şu anda "şimdi topla, sonra şifrele" saldırılarına karşı direnç sağlamak için **X25519** ile **ML-KEM**'i birleştiren hibrit kuantum sonrası (PQ) kriptografik şemaları tanıtıyor.

#### Garlic Messages

Garlic mesajları, bağımsız teslimat talimatlarına sahip birden fazla şifrelenmiş "karanfili" gruplandırarak onion routing'i genişletir. Bunlar mesaj düzeyinde yönlendirme esnekliği ve tek tip trafik doldurma sağlar.

#### Session Tags

Uçtan uca şifreleme için iki kriptografik sistem desteklenmektedir:

- **ElGamal/AES+SessionTags (eski):**  
  Önceden teslim edilen oturum etiketlerini 32-baytlık nonce'lar olarak kullanır. Verimsizliği nedeniyle artık kullanımdan kaldırılmıştır.

- **ECIES-X25519-AEAD-Ratchet (güncel):**  
  ChaCha20-Poly1305 ve senkronize HKDF tabanlı PRNG'ler kullanarak geçici oturum anahtarları ve 8 baytlık etiketleri dinamik olarak üretir, ileri gizliliği korurken CPU, bellek ve bant genişliği yükünü azaltır.

---

## Future of the Protocol

Temel araştırma alanları, devlet düzeyindeki düşmanlara karşı güvenliği koruma ve kuantum sonrası korumalar getirme üzerine odaklanmaktadır. İki erken tasarım konsepti — **kısıtlı rotalar** ve **değişken gecikme** — modern gelişmelerle geride bırakılmıştır.

### Restricted Route Operation

Orijinal kısıtlı yönlendirme (restricted routing) kavramları, IP adreslerini gizlemeyi amaçlıyordu. Bu ihtiyaç büyük ölçüde şu faktörler tarafından azaltılmıştır:

- Otomatik port yönlendirme için UPnP  
- SSU2'de güçlü NAT geçişi  
- IPv6 desteği  
- İşbirlikçi introducers ve NAT delik delme  
- İsteğe bağlı overlay (örn. Yggdrasil) bağlantısı

Bu nedenle, modern I2P aynı hedeflere karmaşık kısıtlı yönlendirme olmadan daha pratik bir şekilde ulaşır.

---

## Similar Systems

I2P, mesaj odaklı ara katman yazılımları, DHT'ler ve mixnet'lerden kavramları entegre eder. İnovasyonu, bunları kullanılabilir, kendi kendini organize eden bir anonimlik platformunda birleştirmesinde yatmaktadır.

### Taşıma Protokolleri

*[Website](https://www.torproject.org/)*

**Tor** ve **I2P** aynı hedefleri paylaşır ancak mimari olarak farklıdır:

- **Tor:** Devre anahtarlamalı; güvenilir dizin yetkililerine dayanır. (~10k röle)  
- **I2P:** Paket anahtarlamalı; tamamen dağıtık DHT-tabanlı ağ. (~50k router)

I2P'nin tek yönlü tünelleri daha az metadata açığa çıkarır ve esnek yönlendirme yollarına izin verirken, Tor anonim **İnternet erişimine (outproxying)** odaklanır. I2P bunun yerine anonim **ağ içi barındırmayı** destekler.

### Kriptografi

*[Web Sitesi](https://freenetproject.org/)*

**Freenet** anonim, kalıcı dosya yayınlama ve alma odaklıdır. Buna karşılık **I2P**, etkileşimli kullanım (web, sohbet, torrent'ler) için **gerçek zamanlı bir iletişim katmanı** sağlar. İki sistem birlikte birbirini tamamlar — Freenet sansüre dayanıklı depolama sağlar; I2P aktarım anonimliği sağlar.

### Other Networks

- **Lokinet:** Teşvikli servis düğümleri kullanan IP tabanlı kaplama ağı.  
- **Nym:** Daha yüksek gecikme süresinde örtü trafiği ile metadata korumasını vurgulayan yeni nesil mixnet.

---

## Appendix A: Application Layer

I2P'nin kendisi yalnızca mesaj taşıma işlemini yönetir. Uygulama katmanı işlevselliği, API'ler ve kütüphaneler aracılığıyla harici olarak uygulanır.

### Streaming Library {#streaming}

**Streaming kütüphanesi**, I2P'nin TCP benzeri işlevi görür; kayan pencere protokolü ve yüksek gecikmeli anonim aktarım için optimize edilmiş tıkanıklık kontrolü ile çalışır.

Tipik HTTP istek/yanıt kalıpları, mesaj paketleme optimizasyonları sayesinde genellikle tek bir gidiş-dönüşte tamamlanabilir.

### Naming Library and Address Book

*Geliştiriciler: mihi, Ragnarok*   [İsimlendirme ve Adres Defteri](/docs/overview/naming) sayfasına bakın.

I2P'nin isimlendirme sistemi **yerel ve merkeziyetsizdir**, DNS tarzı global isimlerden kaçınır. Her router, insan tarafından okunabilir isimlerin destination'lara (hedeflere) yerel bir eşleştirmesini tutar. İsteğe bağlı web-of-trust (güven ağı) tabanlı adres defterleri, güvenilir eşlerden paylaşılabilir veya içe aktarılabilir.

Bu yaklaşım, merkezi otoritelerden kaçınır ve küresel veya oylama tarzı isimlendirme sistemlerinde bulunan Sybil güvenlik açıklarını atlatır.

### Kısıtlı Rota İşlemi

*Geliştiren: mihi*

**I2PTunnel**, anonim TCP proxy'lemeyi sağlayan ana istemci katmanı arayüzüdür. Şunları destekler:

- **İstemci tünelleri** (I2P hedeflerine giden)  
- **HTTP istemcisi (eepproxy)** ".i2p" alan adları için  
- **Sunucu tünelleri** (I2P'den yerel bir hizmete gelen)  
- **HTTP sunucu tünelleri** (web hizmetlerini güvenli bir şekilde proxy'leme)

Outproxy (normal İnternet'e erişim) isteğe bağlıdır ve gönüllüler tarafından çalıştırılan "sunucu" tünelleri ile sağlanır.

### I2PSnark {#i2psnark}

*Geliştirici: jrandom ve diğerleri — [Snark](http://www.klomp.org/snark/) uyarlaması*

I2P ile birlikte gelen **I2PSnark**, DHT ve UDP desteği olan anonim bir çoklu-torrent BitTorrent istemcisidir ve web arayüzü üzerinden erişilebilir.

### Tor

*Geliştiriciler: postman, susi23, mastiejaner*

**I2Pmail**, I2PTunnel bağlantıları üzerinden anonim e-posta sağlar. **Susimail**, geleneksel e-posta istemcilerinde yaygın olan bilgi sızıntılarını önlemek için özel olarak tasarlanmış web tabanlı bir istemcidir. [mail.i2p](https://mail.i2p/) hizmeti, ek koruma için virüs filtreleme, [hashcash](https://en.wikipedia.org/wiki/Hashcash) kotaları ve outproxy ayrımı özellikleri sunar.

---
