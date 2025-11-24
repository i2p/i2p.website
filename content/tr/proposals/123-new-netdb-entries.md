```markdown
---
title: "Yeni netDB Girdileri"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Açık"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Durum

Bu önerinin bazı bölümleri tamamlanmış ve 0.9.38 ve 0.9.39 sürümlerinde uygulanmıştır. Ortak Yapılar, I2CP, I2NP ve diğer spesifikasyonlar, şu anda desteklenen değişiklikleri yansıtacak şekilde güncellenmiştir.

Tamamlanmış bölümler hala küçük revizyonlara tabi olabilir. Bu önerinin diğer bölümleri hala geliştirme aşamasındadır ve önemli revizyonlara tabi olabilir.

Hizmet Araması (tip 9 ve 11) düşük öncelikli ve planlanmamış olup, ayrı bir öneriye bölünebilir.


## Genel Bakış

Bu, aşağıdaki 4 önerinin güncellenmesi ve birleştirilmesidir:

- 110 LS2
- 120 Meta LS2 çoklu barındırma için
- 121 Şifrelenmiş LS2
- 122 Kimlik doğrulanmamış servis araması (yayınlama)

Bu öneriler genellikle bağımsızdır, ancak sağduyu için birkaç tanesi için ortak bir format tanımlayıp kullanırız.

Aşağıdaki öneriler biraz ilgilidir:

- 140 Görünmez Çoklu Barındırma (bu öneriyle uyumsuz)
- 142 Yeni Kripto Şablonu (yeni simetrik kripto için)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 Şifrelenmiş LS2 için B32
- 150 Garlic Farm Protokolü
- 151 ECDSA Körleştirme


## Öneri

Bu öneri, 5 yeni DatabaseEntry türünü ve bunları ağ veritabanına kaydetme ve oradan geri alma sürecini, ayrıca bunları imzalama ve o imzaları doğrulama yöntemini tanımlar.

### Hedefler

- Geriye dönük uyumlu
- Eski tarz çoklu barındırma ile kullanılabilen LS2
- Destek için yeni kripto veya ilkel gerektirmez
- Kripto ve imzalamayı bağımsız tutun; tüm mevcut ve gelecek versiyonları destekleyin
- Opsiyonel çevrimdışı imzalama anahtarlarını etkinleştir
- Parmak izi oluşturmayı azaltmak için zaman damgalarının doğruluğunu azalt
- Hedefler için yeni kripto teknikleri etkinleştir
- Büyük ölçekli çoklu barındırmayı etkinleştir
- Mevcut şifrelenmiş LS ile ilgili birden fazla sorunu düzelt
- Floodfill'lerin görünürlüğünü azaltmak için opsiyonel körleştirme
- Şifrelenmiş, tek anahtar ve birden fazla iptal edilebilir anahtar destekler
- Outproxy aramalarının ve uygulama DHT başlatmanın ve diğer kullanım durumlarının daha kolay araması için servis araması
- 32 baytlık ikili hedef karmasına dayanan herhangi bir şeyi bozmayın, örneğin bittorrent
- Routerinfos'da sahip olduğumuz gibi kiraları esneklik katın.
- Yayınlanan zaman damgası ve değişken sona erme tarihinde başlığı ekleyin, böylece içerikler şifrelenmiş olsa bile çalışır (en erken kiradan zaman damgası çıkarmayın)
- Tüm yeni türler, kullanıcının eski LS'den LS2'ye geçmesine veya LS2, Meta ve Şifrelenmiş arasında değiştirmesine izin vermek için aynı DHT alanında ve aynı konumlarda bulunur, Hedefi veya karmayı değiştirmeden.
- Mevcut bir Hedef, çevrimdışı anahtarlar kullanacak şekilde değiştirilebilir veya çevrimiçi anahtarlara geri dönüştürülebilir, Hedefi veya karmayı değiştirmeden.


### Hedef Dışı / Kapsam Dışı

- Yeni DHT rotasyon algoritması veya paylaşılan rastgele üretim
- Kullanılacak yeni şifreleme türü ve uçtan uca şifreleme şeması ayrı bir öneride yer alacaktır. 
  Burada yeni bir kripto belirtilmemiş veya tartışılmamıştır.
- RIs veya tünel yapımı için yeni şifreleme. 
  Bu ayrı bir öneride ele alınacaktır.
- I2NP DLM / DSM / DSRM mesajlarının şifrelenmesi, iletimi ve alımı yöntemleri. 
  Değiştirilmiyor.
- Meta'yı oluşturma ve destekleme yöntemleri, arka uçlar arası iletişim, yönetim, yedekleme ve koordinasyon dahil.
  İ2CP'ye, veya i2pcontrol'a veya yeni bir protokole destek eklenebilir.
  Bu standartlaşmış olabilir veya olmayabilir.
- Daha uzun sona eren tünellerin gerçekten uygulanması veya mevcut tünellerin iptali için yöntemler. 
  Bu son derece zordur ve olmadan makul bir zarif kapanış yapamazsınız.
- Tehdit modeli değişiklikleri
- Çevrimdışı depolama formatı, veya verileri depolama/geri alma/paylaşma yöntemleri.
- Özellikler burada tartışılmadı ve her projeye bırakıldı.


### Gerekçe

LS2, şifreleme türünü değiştirmek ve gelecekteki protokol değişiklikleri için alanlar ekler.

Şifrelenmiş LS2, mevcut şifrelenmiş LS ile ilgili birkaç güvenlik sorununu
kiraların tamamını asimetrik şifreleme kullanarak giderir.

Meta LS2, esnek, verimli, etkili ve büyük ölçekli çoklu barındırma sağlar.

Hizmet Kaydı ve Hizmet Listesi, adlandırma aramalarını ve DHT başlatmalarını sağlayan
herhangi yayın hizmetleri sunar.


### NetDB Veri Türleri

Tür numaraları, I2NP Veritabanı Arama/Saklama Mesajlarında kullanılır.

Uçtan uca sütun, sorguların/yanıtların bir Sarımsak Mesajındaki bir Hedefe gönderilip gönderilmediğini belirtir.


Mevcut türler:

            NetDB Verileri            Arama Türü   Saklama Türü 
herhangi bir                          0           herhangi bir     
LS                                    1            1      
RI                                    2            0      
keşif                               3           DSRM    

Yeni türler:

            NetDB Verileri            Arama Türü   Saklama Türü   Std. LS2 Başlığı?   Uçtan uca gönderilen?
LS2                                   1            3             evet                 evet
Şifrelenmiş LS2                       1            5             hayır                hayır
Meta LS2                              1            7             evet                 hayır
Hizmet Kaydı                         n/a           9             evet                 hayır
Hizmet Listesi                        4           11             hayır                hayır



Notlar
`````
- Şu anda Arama türleri Veritabanı Arama Mesajındaki bit 3-2'dir.
  Ek türler bit 4'ün kullanımını gerektirecektir.

- Tüm saklama türleri, eski router'lar tarafından Veri Tabanı Saklama Mesajı tür alanındaki üst bitler yok sayıldığından tektir.
  Analystsaklama LS olarak başarısız olmasını daha bitdense bir sıkıştırılmış RI olmasını tercih ederiz.

- Tür, imza tarafından kapsanan verilerde açık mı, örtük mi yoksa her ikisi de mi olmalı?


### Arama/Saklama süreci

Türler 3, 5 ve 7, standart bir leaseset aramasına (tür 1) yanıt olarak döndürülebilir.
Tür 9, bir aramaya yanıt olarak asla döndürülmez.
Türler 11, yeni bir hizmet arama türüne (tür 11) yanıt olarak döndürülür.

Yalnızca tür 3 bir client-to-client Sarımsak mesajında gönderilebilir.



### Biçim

Türler 3, 7 ve 9 ortak bir formata sahiptir::

  Standart LS2 Başlığı
  - aşağıda tanımlandığı gibi

  Tür-Özel Bölüm
  - Her bölüm için aşağıda tanımlandığı gibi

  Standart LS2 İmzası:
  - imza türüyle gösterildiği uzunluk

Tür 5 (Şifrelenmiş) bir Hedefle başlamaz ve farklı bir formata sahiptir. Aşağıya bakın.

Tür 11 (Hizmet Listesi), birkaç Hizmet Kayıtlarının bir toplamıdır ve farklı bir formata sahiptir. Aşağıya bakın.


### Gizlilik/Güvenlik Hususları

TBD



## Standart LS2 Başlığı

Türler 3, 7 ve 9 aşağıda belirtilen standart LS2 başlığını kullanır:


### Biçim
::

  Standart LS2 Başlığı:
  - Tür (1 bayt)
    Aslında başlıkta yer almıyor, ancak imza tarafından kapsanan verilerin bir parçası.
    Veri Tabanı Saklama Mesajı alanından alın.
  - Hedef (387+ bayt)
  - Yayınlanan zaman damgası (4 bayt, büyük endian, epoch'tan beri saniye, 2106'da taşar)
  - Sona erme (2 bayt, büyük endian) (yayınlanan zaman damgasından saniye cinsinden fark, 18.2 saat maksimum)
  - Bayraklar (2 bayt)
    Bit sırası: 15 14 ... 3 2 1 0
    Bit 0: 0 ise, çevrimdışı anahtar yok; 1 ise, çevrimdışı anahtar var
    Bit 1: 0 ise, standart yayınlanmış leaseset.
           1 ise, yayınlanmamış leaseset. Yayınlanmamalı veya sorguya yanıt olarak gönderilmemelidir. Bu leaseset sona ererse, bit 2 ayarlanmadığı sürece netdb'de yenisi için sorgu yapmayın.
    Bit 2: 0 ise, standart yayınlanmış leaseset.
           1 ise, bu şifrelenmemiş leaseset körleştirilir ve yayınlandığında şifrelenir. Bu leaseset sona ererse, netdb'de körleştirilmiş konumda yenisi için sorgu yapın. Bu bit 1 olarak ayarlanmışsa, bit 1 de 1 olarak ayarlayın. 
           0.9.42 sürümünden itibaren.
    Bitler 3-15: Gelecek kullanımlarla uyumluluk için 0 olarak ayarlayın
  - Eğer bayrak çevrimdışı anahtarlar gösteriyorsa, çevrimdışı imza bölümü:
    Sona erme zaman damgası (4 bayt, büyük endian, epoch'tan beri saniye, 2106'da taşar)
    Geçici imza türü (2 bayt, büyük endian)
    Geçici imza açık anahtarı (imza türü ile belirlenen uzunluk)
    Hedefin genel anahtarı ile sona erme zaman damgası, geçici imza türü ve genel anahtarın imzası,
    hedefin genel anahtarı imza türüyle gösterildiği uzunluk.
    Bu bölüm çevrimdışı oluşturulabilir ve oluşturulmalıdır.


Gerekçe
````````

- Yayınlanmamış/yayınlanmış: Bir veritabanı mağazasını uçtan uca gönderirken,
  gönderici router bu leaseset'in başkalarına gönderilmemesini isteyebilir. Şu anda bu durumu korumak için sezgisel kurallar kullanıyoruz.

- Yayınlanan: leaseset'in 'versiyonunu' belirlemek için gereken karmaşık mantığı değiştirir.
  Şu anda, versiyon son sona eren kiralamanın süresi dolumuyla aynı ve bir yayınlama router'i
  yalnızca eski bir kiralamayı kaldıran bir leaseset yayınladığında, bu sona erme süresini en az 1ms artırmalıdır.

- Sona erme: bir netdb girişinin son sona eren kiralamasından daha erken sona ermesini sağlar.
  LS2 için kullanışlı olmayabilir, burada leaseset'lerin 11 dakikalık maksimum bir sona erme süresiyle kalmaları beklenir ama
  yeni türler için gereken yerlerde (aşağıya bakın Meta LS ve Hizmet Kaydı) gereklidir.

- Çevrimdışı anahtarlar, başlangıçta/gerekli uygulama karmaşıklarının azaltılması için opsiyoneldir.


### Sorunlar

- Zaman damgası doğruluğunu daha da azaltabiliriz (10 dakika?), ancak versiyon numarasını eklemek zorunda kalırız. Bu, çoklu barındırmayı bozabilir, zaman damgasına tamamen ihtiyaç duymuyorsak.

- Alternatif: 3 bayt zaman damgası (epoch / 10 dakika), 1 bayt versiyon, 2 bayt sona erme

- Tür, veri / imza içinde açık, örtük veya her ikisi mi? İmza için "Alan" sabitleri mi?


Notlar
`````

- Router'lar bir LS'yi saniyede birden fazla yayınlamamalıdır.
  Ancak yaparlarsa, yayınlanan LS'nin yayımlanmış zaman damgasını önceden yayınlanmış olanın üzerine 1 artırmalıdır.

- Router uygulamaları geçici anahtarları ve imzayı doğrulamadan saklayabilirler.
  Özellikle floodfill'ler ve uzun süreli bağlantıların her iki ucundaki router'lar bundan yararlanabilir.

- Çevrimdışı anahtarlar ve imzalar yalnızca uzun süreli hedefler, yani sunucular için uygundur, istemciler için değil.



## Yeni DatabaseEntry türleri


### LeaseSet 2

Mevcut LeaseSet'e yapılan değişiklikler:

- Yayınlanan zaman damgası, sona erme zaman damgası, bayraklar ve özellikler ekle
- Şifreleme türü ekle
- İptal anahtarı kaldır

Şununla ara
    Standart LS bayrağı (1)
Şununla sakla
    Standart LS2 türü (3)
Şununla sakla
    Hedefin karması
    Bu karma, ardından günlük "yönlendirme anahtarı" oluşturmak için kullanılır, LS1 gibi
Tipik sona erme
    Düzenli bir LS gibi 10 dakika.
Tarafından yayınlandı
    Hedef

Biçim
``````
::

  Yukarıda belirtilen Standart LS2 Başlığı

  Standart LS2 Türüne Özgü Bölüm
  - Özellikler (Ortak yapılar spesifikasyonunda belirtildiği gibi, yoksa 2 sıfır bayt)
  - Takip edilecek anahtar bölümlerinin sayısı (1 bayt, maksimum TBD)
  - Anahtar bölümler:
    - Şifreleme türü (2 bayt, büyük endian)
    - Şifreleme anahtarı uzunluğu (2 bayt, büyük endian)
      Bu, LS2'yi bilinmeyen şifreleme türleriyle bile çözüp doğrulama yapabilecekleri şekilde açık.
    - Şifreleme anahtarı (belirtilmiş bayt sayısı)
  - Kiralama sayısı (1 bayt)
  - Kiralar (her biri 40 bayt)
    Bunlar, 4 baytlık bir sona erme ile kiralardır,
    epoch'tan elde edilen saniyeler (2106'da taşar)

  Standart LS2 İmzası:
  - İmza
    Bayrak, çevrimdışı anahtarları gösteriyorsa, geçici genel anahtarla imzalanır,
    aksi takdirde hedef genel anahtarıyla imzalatılır
    İmza anahtarının imza türüyle gösterilen uzunluk
    İmza, yukarıdaki her şeyin imzasıdır.




Gerekçe
`````````````

- Özellikler: Gelecekteki genişleme ve esneklik.
  Kalan verilerin ayrıştırılması için gerekli olması durumunda ilk kısım haline getirilmiştir.

- Şifreleme türü/kamusal anahtar çiftlerinin çeşitleri
  yeni şifreleme türlerine geçişi kolaylaştırmak içindir. Diğer bir yol ise,
  şifreleme türleri paralel kullanılarak, muhtemelen aynı tüneller kullanılarak,
  deneme/diyadalım ile her anahtarla deneme başlatmaktır. Gelen şifreleme türünü tanımlama
  mevcut seansı yongolemekle ve/veya her anahtarla deneme alını ile gerçekleştirilbilir.
  Gelen mesajların uzunlukları da bir ipucu sağlayabilir.

Tartışma
````````

Bu öneri, son-tarih şifreleme anahtarı için leaseset'in genel anahtarını kullanmaya devam eder ve leaseset içindeki genel anahtar kullanılmaz.
Şifreleme türü Hedef anahtar sertifikasında belirtilmemiştir, 0 olarak kalacaktır.

Reddedilen bir alternatif, şifreleme türünü Hedef Anahtar sertifikasından belirtmek,
Hedef içindeki genel anahtarı kullanmak ve leaseset içindeki genel anahtarı kullanmamaktı. 
Bunu yapmayı planlamıyoruz.

LS2'nin Avantajları:

- Gerçek genel anahtarın konumu değişmez.
- Hedefi değiştirmeden, şifreleme türü veya genel anahtar değişebilir.
- Kullanılmayan iptal alanının kaldırılması
- Bu önerideki diğer DatabaseEntry türleriyle temel uyumluluk
- Birden fazla şifreleme türüne olanak tanır

LS2'nin Dezavantajları:

- Genel anahtar ve şifreleme türünün konumu RouterInfo'dan farklıdır
- Leaseset'de kullanılmayan genel anahtarı korur
- Ağ genelinde uygulama gerektirir; alternatif olarak deneysel
  şifreleme türleri ağ geçişleri tarafından ne süreye kadar kullanılabilir
  (ancak bkz. ilgili 136 ve 137 numaralı öneriler, deneysel imza türü desteği hakkında).
  Deneysel şifreleme türleri için uygulamak ve test etmek alternatif öneritatı daha kolay olabilir.


Yeni Şifreleme Sorunları
``````````````````````````
Bir kısmı bu önerinin kapsamı dışında,
ancak şimdi öneri verirken notları buraya bırakıyoruz çünkü
şu an için ayrı bir şifreleme önerimiz yok.
Ayrıca ECIES önerileri 144 ve 145'e bakın.

- Şifreleme türü, eğri, anahtar uzunluğu ve uçtan uca şema
  dahil olmak üzere KDF ve MAC, eğer varsa bir kombinasyonu hizmet eder.

- Bilinmeyen şifreleme türleri için bile LS2'yi ayrıştırabilir ve doğrulayabilir
  olması için bir anahtar uzunluğu alanı ekledik.

- Önerilecek yeni şifreleme türünün ilk hamlesi muhtemelen 
  ECIES/X25519 olacaktır. Uçtan uca kullanılabilecek
  (ElGamal/AES+SessionTag'ın hafif modifikasyonu ya da tamamen yeni bir şey, örneğin ChaCha/Poly)
  biri veya birkaç ayrı öneride belirtilecektir.
  Ayrıca ECIES önerilieri 144 ve 145'e de bakın.


Notlar
`````
- Kiralamalarda 8 baytlık sona etlafenler 4 bayta değiştirildi.

- İptal gerçekleştirme alanı yerine, sona ermesi sıfır olan bir tarihle yapabiliriz,
  veya sıfır kiralamalar veya her ikisi birden. 
  Ayrı bir iptal anahtarı gerekmez.

- Şifreleme anahtarları, çoğunlukla sunucu tercih sırasına göre sıralanmıştır,
  en çok tercih edilen ilk sırada yer alır. 
  Varsayılan istemci davranışı, desteklenen şifreleme türüne sahip
   birinci anahtarı seçmektir.
  İstemciler şifreleme desteğe, göreli performans ve diğer faktörlere dayalı olarak

`````
