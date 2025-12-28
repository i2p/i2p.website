---
title: "ECIES Yönlendiricileri"
number: "156"
author: "zzz, orijinal"
created: "2020-09-01"
lastupdated: "2025-03-05"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2950"
target: "0.9.51"
toc: true
---

## Not
Ağ dağıtımı ve test yapılmaktadır.
Revizyona tabidir.
Durum:

- ECIES Yönlendiricileri 0.9.48 itibarıyla uygulanmıştır, bkz. [Ortak](/docs/specs/common-structures/).
- Tünel oluşturma 0.9.48 itibarıyla uygulanmıştır, bkz. [Tünel-Oluşumu-ECIES](/docs/specs/implementation/#tunnel-creation-ecies).
- ECIES yönlendiricilerine şifrelenmiş mesajlar 0.9.49 itibarıyla uygulanmıştır, bkz. [ECIES-YÖNLENDİRİCİLER](/docs/specs/ecies-routers/).
- Yeni tünel oluşturma mesajları 0.9.51 itibarıyla uygulanmıştır.


## Genel Bakış


### Özet

Yönlendirici Kimlikleri şu anda bir ElGamal şifreleme anahtarı içermektedir.
Bu, I2P'nin başlangıcından beri standart olmuştur.
ElGamal yavaştır ve kullanıldığı her yerde değiştirilmelidir.

LS2 [Öneri123](/proposals/123-new-netdb-entries/) ve ECIES-X25519-AEAD-Ratchet [Öneri144](/proposals/144-ecies-x25519-aead-ratchet/) (şimdi [ECIES](/docs/specs/ecies/)'de belirtilmiştir) için yapılan öneriler, ElGamal'ın Hedefler için ECIES ile değiştirilmesini tanımlamıştır.

Bu öneri, ElGamal'ın yönlendiriciler için ECIES-X25519 ile değiştirilmesini tanımlar. Bu öneri, gereken değişikliklerin genel bir özetini sağlar. Detayların çoğu diğer önerilerde ve spesifikasyonlardadır. Bağlantılar için referans bölümüne bakın.


### Hedefler

Ek hedefler için [Öneri152](/proposals/152-ecies-tunnels/)’yı inceleyin.

- Yönlendirici Kimliklerinde ElGamal'ı ECIES-X25519 ile değiştir
- Mevcut kriptografik ilkelere yeniden kullan
- Tünel oluşturma mesaj güvenliğini mümkün olduğunca artırırken uyumluluğu koru
- ElGamal/ECIES eşleri karıştırılmış tünelleri destekle
- Mevcut ağ ile maksimum uyumluluğu sağla
- Tüm ağa "bayrak günü" güncellemesini gerektirme
- Riski en aza indirmek için kademeli dağıtım
- Yeni, daha küçük tünel oluşturma mesajı


### Hedef Olmayanlar

Ek hedef olmayanlar için [Öneri152](/proposals/152-ecies-tunnels/)’yı inceleyin.

- Çift anahtar gerektiren yönlendiriciler için gereksinim yok
- Katman şifrelemesi değişiklikleri, bunun için [Öneri153](/proposals/153-chacha20-layer-encryption/)’ye bakın


## Tasarım


### Anahtar Konumu ve Kripto Türü

Hedefler için, anahtar Hedefte değil leaseset içindedir ve aynı leaseset içinde birden fazla şifreleme türünü destekleriz.

Bu yönlendiriciler için gerekli değildir. Yönlendiricinin şifreleme anahtarı Yönlendirici Kimliğinde yer alır. Ortak yapılar spesifikasyonuna bakın [Ortak](/docs/specs/common-structures/).

Yönlendiriciler için, Yönlendirici Kimliği'ndeki 256 baytlık ElGamal anahtarını 32 baytlık X25519 anahtarı ve 224 baytlık dolgu ile değiştireceğiz. Bu, anahtar sertifikasındaki kripto türü ile belirtilir. Kripto türü (LS2'de kullanılanla aynı) 4'tür. Bu, küçük uçlu sıralı 32 baytlık X25519 genel anahtarı belirtir. Bu, ortak yapılar spesifikasyonunda tanımlanan standart yapıdır [Ortak](/docs/specs/common-structures/).

Bu, öneri 145'teki (Öneri145) kripto türleri 1-3 için önerilen ECIES-P256 yöntemine özdeş [Öneri145](/proposals/145-ecies/). Bu öneri hiçbir zaman kabul edilmemesine rağmen, Java uygulama geliştiricileri kod tabanının çeşitli yerlerine kontroller ekleyerek Yönlendirici Kimliği anahtar sertifikalarındaki kripto türleri için hazırlanmışlardı. Bu işlerin çoğu 2019 ortasında yapıldı.


### Tünel Oluşturma Mesajı

ECIES yerine ElGamal kullanmak için tünel oluşturma spesifikasyonunda [Tünel-Oluşumu](/docs/specs/implementation/#tunnel-creation-ecies) çeşitli değişiklikler gereklidir. Ayrıca, tünel oluşturma mesajlarının güvenliğini artırmak için geliştirmeler yapacağız.

Birinci aşamada, ECIES geçişleri için Oluşturma İstek Kaydı ve Oluşturma Yanıt Kaydı'nın formatını ve şifrelemesini değiştireceğiz. Bu değişiklikler mevcut ElGamal yönlendiricilerle uyumlu olacak. Bu değişiklikler öneri 152'de tanımlanmıştır [Öneri152](/proposals/152-ecies-tunnels/).

İkinci aşamada, Oluşturma İstek Mesajı, Oluşturma Yanıt Mesajı, Oluşturma İstek Kaydı ve Oluşturma Yanıt Kaydı'nın yeni bir sürümünü ekleyeceğiz. Verimlilik için boyut küçültülecektir. Bu değişikliklerin bir tüneldeki tüm geçişler tarafından desteklenmesi gerekir ve tüm geçişler ECIES olmalıdır. Bu değişiklikler öneri 157'de tanımlanmıştır [Öneri157](/proposals/157-new-tbm/).


### Uçtan Uca Şifreleme

#### Geçmiş

Orijinal Java I2P tasarımında, yönlendirici ve tüm yerel Hedefler tarafından paylaşılan tek bir ElGamal Oturum Anahtarı Yöneticisi (SKM) vardı. Paylaşılan bir SKM bilgi sızdırabilir ve saldırganlar tarafından korelasyona izin verebilir, bu nedenle tasarım yönlendirici ve her Hedef için ayrı ElGamal SKM'leri desteklemek üzere değiştirildi. ElGamal tasarımı yalnızca anonimsiz göndericileri destekliyordu; gönderici yalnızca geçici anahtarlar gönderiyor, statik bir anahtar değil. Mesaj göndericinin kimliğine bağlanmamıştı.

Daha sonra, ECIES-X25519-AEAD-Ratchet [Öneri144](/proposals/144-ecies-x25519-aead-ratchet/)'de şimdi [ECIES](/docs/specs/ecies/) olarak belirtilen ECIES Ratchet SKM'yi tasarladık. Bu tasarım, göndericinin statik anahtarını ilk mesajda içeren Noise "IK" deseni kullanılarak belirtilmiştir. Bu protokol ECIES (tip 4) Hedefler için kullanılır. IK deseni anonim göndericilere izin vermez.

Bu nedenle, öneriye bir Ratchet SKM'ye anonim mesajlar gönderme yolunu da dahil ettik, sıfır dolu bir statik anahtar kullanarak. Bu, bir Noise "N" deseni simülasyonu yaptı, ancak uyumlu bir şekilde, böylece bir ECIES SKM hem anonim hem de anonim olmayan mesajları alabilir. Amacı ECIES yönlendiricileri için sıfır anahtar kullanmaktı.


#### Kullanım Durumları ve Tehdit Modelleri

Yönlendiricilere gönderilen mesajlar için kullanım durumu ve tehdit modeli, Hedefler arasındaki uçtan uca mesajlaşmadan çok farklıdır.


Hedef kullanım durumu ve tehdit modeli:

- Hedefler arası anonim olmayan (gönderici statik anahtar içeriyor)
- Hedefler arası sürekli trafiği verimli bir şekilde destekleme (tam el sıkışma, akış ve etiketler)
- Her zaman çıkış ve giriş tünelleri üzerinden gönderilir
- OBEP ve IBGW'dan tüm tanımlayıcı karakteristikleri gizleme, geçici anahtarların Elligator2 kodlamasını gerektirir.
- Her iki katılımcı da aynı şifreleme türünü kullanmalıdır


Yönlendirici kullanım durumu ve tehdit modeli:

- Yönlendiricilerden veya hedeflerden anonim mesajlar (gönderici statik anahtar içermez)
- Yalnızca şifrelenmiş Veritabanı Aramaları ve Mağazaları için, genellikle floodfill'ler için
- Nadiren mesajlar
- Birden fazla mesajın korelationu yapılmamalı
- Her zaman doğrudan bir yönlendiriciye giden çıkış tüneli üzerinden gönderilir. Hiçbir giriş tüneli kullanılmaz
- OBEP, bir mesajı bir yönlendiriciye yönlendirdiğini bilir ve şifreleme türünü bilir
- İki katılımcı farklı şifreleme türlerine sahip olabilir
- Veritabanı Arama yanıtları, Veritabanı Arama mesajındaki yanıt anahtarı ve etiketi kullanarak tek seferlik mesajlar
- Veritabanı Mağazasının onayları, birleştirilmiş Teslim Durumu mesajı kullanarak tek seferlik mesajlar


Yönlendirici kullanım olayı hedef-olmayanlar:

- Anonim olmayan mesajlar için ihtiyaç yok
- Giriş araştırma tünelleri yoluyla mesaj göndermek için ihtiyaç yok (bir yönlendirici araştırma leaseset'leri yayınlamaz)
- Etiket kullanarak sürekli mesaj trafiğine ihtiyaç yok
- Hedefler için [ECIES](/docs/specs/ecies/)de açıklanan "çift anahtar" Oturum Anahtarı Yöneticilerini çalıştırmaya gerek yok. Yönlendiricilerin yalnızca bir genel anahtarı vardır.


#### Tasarım Sonuçları

ECIES Yönlendirici SKM'nin [ECIES](/docs/specs/ecies/)de Hedefler için belirtilen tam bir Ratchet SKM'ye ihtiyacı yoktur.
IK desenini kullanarak anonim olmayan mesajlar için gereklilik yoktur.
Tehdit modeli, Elligator2 kodlu geçici anahtarlar gerektirmez.

Bu nedenle, yönlendirici SKM, tünel oluşturma için [Öneri152](/proposals/152-ecies-tunnels/)de belirtildiği gibi Noise "N" desenini kullanacaktır.
Hedefler için [ECIES](/docs/specs/ecies/)de belirtilen aynı yük formatını kullanacaktır.
IK'da [ECIES](/docs/specs/ecies/)de belirtilen sıfır statik anahtar (bağlantısız veya oturumsuz) modu kullanılmayacaktır.

Aramalara yanıtlar, aramada istenirse bir ratchet etiketi ile şifrelenecektir.
Bu, [Öneri154](/proposals/154-ecies-lookups/), şimdi [I2NP](/docs/specs/i2np/)de belirtilmiştir.

Tasarım, yönlendiricinin tek bir ECIES Oturum Anahtarı Yöneticisi'ne sahip olmasını sağlar.
Hedefler için [ECIES](/docs/specs/ecies/)de açıklanan "çift anahtar" Oturum Anahtarı Yöneticilerini çalıştırmaya gerek yoktur.
Yönlendiricilerin yalnızca bir genel anahtarı vardır.

Bir ECIES yönlendiricisinin ElGamal statik anahtarı yoktur.
Yönlendiricinin, ElGamal yönlendiricileri aracılığıyla tünel oluşturmak ve ElGamal yönlendiricilerine şifreli mesajlar göndermek için bir ElGamal uygulamasına ihtiyacı vardır.

Bir ECIES yönlendirici, bir ElGamal tagged mesajlarının alındığı yanıtlar için kısmi bir ElGamal Oturum Anahtarı Yöneticisine gereksinim duyabilir
pre-0.9.46 floodfill yönlendiricilerden gelen NetDB aramalarına yanıtlar bekleniyor, çünkü bu yönlendiriciler hala [Öneri152](/proposals/152-ecies-tunnels/)de belirtilen ECIES-tag yanıtlarının uygulamasına sahip değil.
Aksi takdirde, bir ECIES yönlendirici pre-0.9.46 floodfill yönlendiriciden şifreli bir yanıt talep etmeyebilir.

Bu isteğe bağlıdır. Karar farklı I2P uygulamalarında değişebilir ve
ağın ne kadarının 0.9.46 veya daha yüksek bir sürüme yükseltildiğine bağlı olabilir.
Bu tarih itibarıyla, ağın yaklaşık %85'i 0.9.46 veya daha yüksek bir sürümdedir.


## Spesifikasyon

X25519: [ECIES](/docs/specs/ecies/) 'e bakın.

Yönlendirici Kimliği ve Anahtar Sertifikası: [Ortak](/docs/specs/common-structures/) 'a bakın.

Tünel Oluşturma: [Öneri152](/proposals/152-ecies-tunnels/) 'ye bakın.

Yeni Tünel Oluşturma Mesajı: [Öneri157](/proposals/157-new-tbm/) 'ye bakın.


### İstek Şifreleme

İstek şifrelemesi, Noise "N" deseni kullanarak [Tünel-Oluşumu-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) ve [Öneri152](/proposals/152-ecies-tunnels/) 'de belirtilen aynıdır.

Aramalara yanıtlar, aramada istenirse bir ratchet etiketi ile şifrelenecektir.
Veritabanı Arama istek mesajları, [I2NP](/docs/specs/i2np/) ve [Öneri154](/proposals/154-ecies-lookups/) 'de belirtildiği gibi 32 baytlık yanıt anahtarı ve 8 baytlık yanıt etiketi içerir. Anahtar ve etiket yanıtı şifrelemek için kullanılır.

Etiket setleri oluşturulmaz.
ECIES-X25519-AEAD-Ratchet [Öneri144](/proposals/144-ecies-x25519-aead-ratchet/) ve [ECIES](/docs/specs/ecies/) 'de belirtilen sıfır statik anahtar şeması kullanılmayacaktır.
Geçici anahtarlar Elligator2 ile kodlanmayacaktır.

Genellikle, bunlar Yeni Oturum mesajları olacak ve sıfır statik anahtar ile (bağlantısız veya oturumsuz) gönderilecektir, çünkü mesajın göndericisi anonimdir.


#### Başlangıç ck ve h için KDF

Bu, standart [NOISE](https://noiseprotocol.org/noise.html) "N" deseni için standart bir protokol adı ile.
Bu, tünel oluşturma mesajları için [Tünel-Oluşumu-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) ve [Öneri152](/proposals/152-ecies-tunnels/) 'de belirtilen ile aynıdır.


  ```text

Bu, "e" mesaj deseni:

  // Protokol adını tanımla.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bayt, US-ASCII kodlu, NULL sonlandırılması yok).

  // Karma h = 32 bayt tanımla
  // 32 bayta padle. 32 bayttan fazla olmadığı için hashleme.
  h = protocol_name || 0

  32 bayt zincirleme anahtarını tanımla. h verilerini ck'ye kopyala.
  ZincirlemeAnahtar = h olarak ayarla

  // MixHash(null prologue)
  h = SHA256(h);

  // buraya kadar, tüm yönlendiriciler tarafından önceden hesaplanabilir.


  ```


#### Mesaj için KDF

Mesaj yaratıcıları her mesaj için geçici bir X25519 anahtar çifti oluştururlar.
Geçici anahtarlar mesaj başına benzersiz olmalıdır.
Bu, tünel oluşturma mesajları için [Tünel-Oluşumu-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) ve [Öneri152](/proposals/152-ecies-tunnels/) 'de belirtilen ile aynıdır.


  ```dataspec


// Hedef yönlendiricinin X25519 statik anahtar çifti (hesk, hepk) Yönlendirici Kimliğinden
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || aşağıda ekle
  h = SHA256(h || hepk);

  // buraya kadar, her yönlendirici tarafından önceden hesaplanabilir
  // tüm gelen mesajlar için

  // Gönderici bir X25519 geçici anahtar çifti oluşturur
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  "e" mesaj deseninin sonu.

  Bu, "es" mesaj desenidir:

  // Noise es
  // Gönderici alıcının statik kamu anahtarı ile bir X25519 DH yapar.
  // Hedef yönlendirici
  // şifreli kayıttan önce göndericinin geçici anahtarını çıkarır.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Şifrele/deşifrele için ChaChaPoly parametreleri
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Zincir anahtarı kullanılmaz
  //chainKey = keydata[0:31]

  // AEAD parametreleri
  k = keydata[32:63]
  n = 0
  düz metin = 464 bayt oluşturma istek kaydı
  ad = h
  şifreli metin = ENCRYPT(k, n, düz metin, ad)

  "es" mesaj deseninin sonu.

  // MixHash(şifreli metin) gerekli değil
  //h = SHA256(h || şifreli metin)


  ```


#### Yük

Yük, [ECIES](/docs/specs/ecies/) ve [Öneri144](/proposals/144-ecies-x25519-aead-ratchet/) 'de tanımlanan aynı blok formatıdır.
Tüm mesajlar, tekrarlamayı önlemek için bir TarihSaat bloğu içermelidir.


### Yanıt Şifreleme

Veritabanı Arama mesajlarına yanıtlar, Veritabanı Mağaza veya Veritabanı Arama Yanıtı mesajlarıdır.
Bunlar, [I2NP](/docs/specs/i2np/) ve [Öneri154](/proposals/154-ecies-lookups/) 'de belirtildiği gibi
32 baytlık yanıt anahtarı ve 8 baytlık yanıt etiketi ile Mevcut Oturum mesajları olarak şifrelenir.


Veritabanı Mağaza mesajlarına doğrudan yanıtlar yoktur. Gönderen, kendine bir Sarımsak Mesajı olarak kendi yanıtını içeren bir Teslim Durumu mesajı olarak ekleyebilir.


## Gerekçe

Bu tasarım, mevcut kriptografik ilkelere, protokollere ve kodlara yeniden kullanımı maksimize eder.

Bu tasarım riski en aza indirir.


## Uygulama Notları

Eski yönlendiriciler, yönlendiricinin şifreleme türünü kontrol etmez ve ElGamal ile şifrelenmiş
oluşturma kayıtları ya da netdb mesajları gönderir.
Bazı yeni yönlendiriciler hatalıdır ve çeşitli türlerde bozulmuş
oluşturma kayıtları gönderir.
Bazı yeni yönlendiriciler isteğe bağlı olmayan (tam ratchet) netdb mesajları gönderebilir.
Yarar uygulayıcılar, bu kayıtları ve mesajları mümkün olduğu kadar erken tespit etmeli ve reddetmeli
ve işlemci kullanımını azaltmalı.


## Sorunlar

Öneri 145 [Öneri145](/proposals/145-ecies/), çoğunlukla Öneri 152 [Öneri152](/proposals/152-ecies-tunnels/)
ile uyumlu olacak şekilde yeniden yazılabilir veya yazılamaz.


## Geçiş

Uygulama, test ve yerleştirme birkaç sürüm alacak
ve yaklaşık bir yıl sürecektir. Aşamalar aşağıdaki gibidir.
Her aşamanın belirli bir sürüme atanması, geliştirme hızına bağlı olarak belirlenecektir.

Uygulama ve geçişin detayları her I2P uygulaması için farklı olabilir.


### Temel Noktadan Noktaya

ECIES yönlendiricileri ElGamal yönlendiricilerle bağlanabilir ve bağlantıları alabilir.
Bu şimdi mümkün olmalıdır, çünkü ön tamamlanmamış öneri 145'e [Öneri145](/proposals/145-ecies/) mid-2019'da
Java kod tabanına bir dizi kontrol eklenmiştir.
ElGamal olmayan yönlendiricilere nokta-nokta bağlantılarını engelleyen
hiçbir şeyin olmadığından emin olun.

Kod doğruluğu kontrolleri:

- ElGamal yönlendiricilerin Veritabanı Arama mesajlarına AEAD şifreli yanıtları talep etmediğinden emin olun
  (yanıt bir araştırma tünelinden yönlendiriciye geri geldiğinde)
- ECIES yönlendiricilerin Veritabanı Arama mesajlarına AES şifreli yanıtları talep etmediğinden emin olun
  (yanıt bir araştırma tünelinden yönlendiriciye geri geldiğinde)

Spesifikasyonlar ve uygulamalar tamamlanana kadar:

- ElGamal yönlendiricilerin ECIES yönlendiricileri üzerinden tünel oluşturmayı denemediğinden emin olun.
- ElGamal yönlendiricilerin ECIES floodfill yönlendiricilerine şifrelenmiş ElGamal mesajlar göndermediğinden emin olun.
  (Veritabanı Aramaları ve Veritabanı Mağazaları)
- ECIES yönlendiricilerin ElGamal floodfill yönlendiricilerine şifrelenmiş ECIES mesajlar göndermediğinden emin olun.
  (Veritabanı Aramaları ve Veritabanı Mağazaları)
- ECIES yönlendiricilerin otomatik olarak floodfill olmalarını sağlamak.
Eğer değişiklikler gerekirse, hedef sürüm: 0.9.48


### NetDB Uyumluluğu

ECIES yönlendirici bilgileri ElGamal floodfill'lere depolanabilir ve buradan alınabilir.
Bu şimdi mümkün olmalıdır, çünkü ön tamamlanmamış öneri 145'e [Öneri145](/proposals/145-ecies/)
reaksiyon olarak Java kod tabanına bir dizi kontrol eklenmiştir.
Kod tabanlarında ElGamal olmayan RouterInfos'un ağ veritabanında depolanmasını
engelleyen hiçbir şeyin olmadığından emin olun.

Eğer değişiklikler gerekli ise, hedef sürüm: 0.9.48


### Tünel Oluşturma

Öneri 152'de [Öneri152](/proposals/152-ecies-tunnels/) tanımlandığı gibi tünel oluşturmayı uygulayın.
Kendi yapı istek kaydını kullanarak bir gelen tünel için bir ECIES yönlendiriciyle
tüneller oluşturulmasına başlayarak test edin ve hata ayıklayın.

Daha sonra ElGamal ve ECIES geçişlerinin bir karışımıyla tüneller inşa eden
ECIES yönlendiricilerinin test edilmesini ve desteklenmesini sağlayın.

Daha sonra ECIES yönlendiricileri üzerinden tünel oluşturmayı etkinleştirin.
Macarsız bir sürüm kontrolü gerekli olmamalıdır
eğer öneri 152'ye ait hiç uyumsuz değişiklik bir sürümden sonra yapılırsa.

Hedef sürüm: 0.9.48, 2020 sonları


### ECIES floodfills'e Ratchet mesajları

ECIES mesajlarının (sıfır statik anahtar ile) ECIES floodfill'ler tarafından
alınması için uygulama ve test yapın,
öneri 144'de tanımlandığı gibi [Öneri144](/proposals/144-ecies-x25519-aead-ratchet/).
ECIES yönlendiricileri tarafından Veritabanı Arama mesajlarına AEAD yanıtlarının alınması
uygulama ve testini yapın.

ECIES yönlendiriciler tarafından otomatik floodfill'i etkinleştirin.
Ardından ECIES yönlendiricilerine ECIES mesajlarının gönderilmesini sağlayın.
Eğer öneri 152'ye ait bir uyumsuz değişiklik yapılırsa
ilk piyasaya sürülmeden önce minimum bir sürüm kontrolü gerekli olmamalıdır.

Hedef sürüm: 0.9.49, 2021 başları.
ECIES yönlendiriciler otomatik olarak floodfill olabilir.


### Yeniden Anahtarlama ve Yeni Kurulumlar

Yeni kurulumlar 0.9.49 sürümünden itibaren varsayılan olarak ECIES olacaktır.

Risk ve ağ kesintisini en aza indirgemek için tüm yönlendiricilerin kademeli olarak yeniden anahtarlanması.
Yıllar önceki imza türü geçişi sırasında değişiklik yapan
mevcut kodu kullanın.
Bu kod, her başlatma sırasında bir yönlendiricinin
küçük bir rastgele yeniden anahtarlama şansı vermektedir.
Birkaç başlatma sonrasında, bir yönlendirici muhtemelen ECIES'e yeniden anahtarlanmış olacaktır.

Yeniden anahtarlama kriterleri, ağın yeterli kısmının,
belki %50'sinin, ECIES yönlendiricileri aracılığıyla tünel oluşturmasının mümkün olmasıdır (0.9.48 veya daha yüksek).

Ağın büyük bir kısmının, büyük çoğunluğu
(belki %90 ya da daha fazlası),
ECIES yönlendiricileri aracılığıyla tünel oluşturabilmesi
(0.9.48 veya daha yüksek) VE
ECIES floodfill yönlendiricilere mesaj gönderebilmesi
(0.9.49 veya daha yüksek) sağlanmadan önce tüm ağın agresif şekilde yeniden anahtarlanması gerektir.
Bu hedef muhtemelen 0.9.52 sürümü için ulaşılacaktır.

Yeniden anahtarlama birkaç sürüm alacaktır.

Hedef sürüm:
0.9.49 için yeni yönlendiriciler ECIES'i varsayılan hale getirsin;
0.9.49 için yavaşça yeniden anahtarlamayı başlat;
0.9.50 - 0.9.52 tekrar tekrar yeniden anahtarlama hızını artırmak için;
2021 sonu için ağın çoğunluğu yeniden anahtarlanacak.


### Yeni Tünel Oluşturma Mesajı (Aşama 2)

Öneri 157'de belirtilen [Öneri157](/proposals/157-new-tbm/) yeni Tünel Oluşturma Mesajını uygulayın ve test edin.
0.9.51 sürümünde desteği yayınlayın.
Ek test yapın, ardından 0.9.52 sürümünde etkinleştirin.

Test zor olacaktır.
Bu, geniş çapta test edilmeden önce, ağın iyi bir alt kümesi bunu desteklemelidir.
Geniş çapta faydalı olmadan önce, ağın çoğunluğunun bunu desteklemesi gerekir.
Eğer spesifikasyon veya uygulama değişiklikleri testten sonra gerekirse,
bu, yayımı bir sonraki sürüm için geciktirebilir.

Hedef sürüm: 0.9.52, 2021 sonları.


### Yeniden Anahtarlama Tamamlandı

Bu noktada, bir sürümden daha eski yönlendiriciler TBD,
çoğu eş aracılığıyla tünel oluşturamayacak.

Hedef sürüm: 0.9.53, 2022 başları.


