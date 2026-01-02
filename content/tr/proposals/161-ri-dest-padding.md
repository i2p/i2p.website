---
title: "RI ve Hedef Doldurma"
number: "161"
author: "zzz"
created: "2022-09-28"
lastupdated: "2023-01-02"
status: "Açık"
thread: "http://zzz.i2p/topics/3279"
target: "0.9.57"
toc: true
---

## Durum

0.9.57'de uygulandı.
Bu öneriyi "Gelecek Planlama" bölümündeki fikirleri geliştirmek ve tartışmak için açık bırakıyoruz.


## Genel Bakış


### Özet

ElGamal açık anahtarı, 0.6 sürümünden (2005) beri Hedeflerde kullanılmamaktadır.
Spesifikasyonlarımız bunun kullanılmadığını belirtse de, uygulamaların
bir ElGamal anahtar çifti oluşturmaktan kaçınıp alanı rastgele veriyle doldurabileceğini söylemezler.

Spesifikasyonları değiştirerek
alanın göz ardı edildiğini ve uygulamaların alanı rastgele verilerle doldurabileceğini önermekteyiz.
Bu değişiklik geriye dönük uyumlu. ElGamal açık anahtarını doğrulayan bilinen bir uygulama yoktur.

Ayrıca, bu öneri uygulayıcılar için Hedef VE Yönlendirici Kimliği dolgusu için rastgele verilerin nasıl oluşturulacağı konusunda
güvenli kalırken ve Base 64 gösterimlerinin bozuk veya güvensiz görünmesini önlerken sıkıştırılabilir olmasını sağlamak
için rehberlik sunar. Bu, herhangi bir kesintiye neden olan protokol değişiklikleri olmadan doldurma alanlarını kaldırmanın
çoğu faydasını sağlar. Sıkıştırılabilir Hedefler, akış SYN ve yanıtlanabilir datagram boyutunu azaltır;
sıkıştırılabilir Yönlendirici Kimlikleri, Veritabanı Depolama Mesajlarını, SSU2 Oturum Onaylanmış
mesajlarını ve yeniden tohumlanan su3 dosyalarını azaltır.

Son olarak, öneri tüm doldurmayı tamamen ortadan kaldıracak yeni Hedef ve Yönlendirici Kimlik formatları için
olası seçenekleri tartışır. Gelecek planlamasını etkileyebilecek post-kuantum kriptografisi hakkında kısa bir tartışma da bulunmaktadır.


### Hedefler

- Hedefler için ElGamal anahtar çifti üretme gereksinimini ortadan kaldırma
- Hedeflerin ve Yönlendirici Kimliklerinin oldukça sıkıştırılabilir olmasını 
  sağlamak için en iyi uygulamaları önermek,
  ancak Base 64 gösterimlerinde belirgin desenler göstermemesi
- Bütün uygulamaların en iyi uygulamaları benimsemesini teşvik etmek
  böylece alanlar ayırt edilemez
- Akış SYN boyutunu azaltma
- Yanıtlanabilir datagram boyutunu azaltma
- SSU2 RI blok boyutunu azaltma
- SSU2 Oturum Onaylanmış boyutu ve parçalanma sıklığını azaltma
- Veritabanı Depolama Mesajı (RI ile) boyutunu azaltma
- Yeniden tohumlanan dosya boyutunu azaltma
- Tüm protokoller ve API'lerle uyumu sürdürme
- Spesifikasyonları güncelleme
- Yeni Hedef ve Yönlendirici Kimlik formatları için alternatifleri tartışma

ElGamal anahtarlarının üretim gereksinimini ortadan kaldırarak, uygulamalar 
diğer protokollerde geriye dönük uyumluluk dikkate alınarak ElGamal kodunu tamamen kaldırabilirler.


## Tasarım

Teknik olarak, yalnızca 32 baytlık imzalama açık anahtarı (hem Hedeflerde hem de Yönlendirici Kimliklerinde)
ve 32 baytlık şifreleme açık anahtarı (sadece Yönlendirici Kimliklerinde) bir tür rastgele sayı 
ve bu yapıların SHA-256 hash'lerinin kriptografik olarak güçlü ve ağ veritabanı DHT'sinde rastgele
dağıtılmış olmasını sağlar.

Ancak, ihtiyatlı bir tedbir olarak, ElG açık anahtar alanında ve dolgumda en az 32 bayt rastgele 
veri kullanılmasını öneriyoruz. Ayrıca, alanların tüm sıfırlar olması durumunda,
Base 64 hedefler AAAA karakterlerinin uzun dizilerini içerecek ve bu kullanıcılar için alarm 
veya karışıklığa neden olabilir.

Ed25519 imza türü ve X25519 şifreleme türü için:
Hedefler rastgele verilerin 11 kopyasını (352 bayt) içerir.
Yönlendirici Kimlikleri rastgele verilerin 10 kopyasını (320 bayt) içerir.


### Tahmini Tasarruflar

Hedefler her akış SYN ve yanıtlanabilir datagram içinde
bulunur. Yönlendirici Bilgileri (Yönlendirici Kimlikleri içerir) Veritabanı Depolama Mesajlarında
ve NTCP2 ve SSU2 içindeki Oturum Onaylanmış mesajlarında bulunur.

NTCP2 Yönlendirici Bilgisini sıkıştırmaz.
Veritabanı Depolama Mesajlarındaki RI'lar ve SSU2 Oturum Onaylanmış mesajlar sıkıştırılır.
Yönlendirici Bilgileri yeniden tohumlanan SU3 dosyalarında sıkıştırılır.

Veritabanı Depolama Mesajlarındaki Hedefler sıkıştırılmaz.
Akış SYN mesajları I2CP katmanında sıkıştırılır.

Ed25519 imza türü ve X25519 şifreleme türü için,
tahmini tasarruflar:

| Veri Türü | Toplam Boyut | Anahtarlar ve Sertifika | Sıkıştırılmamış Dolgu | Sıkıştırılmış Dolgu | Boyut | Tasarruflar |
|-----------|--------------|------------------------|----------------------|---------------------|-------|-------------|
| Hedef | 391 | 39 | 352 | 32 | 71 | 320 bayt (82%) |
| Yönlendirici Kimlik | 391 | 71 | 320 | 32 | 103 | 288 bayt (74%) |
| Yönlendirici Bilgisi | 1000 typ. | 71 | 320 | 32 | 722 typ. | 288 bayt (29%) |

Notlar: 7 baytlık sertifikanın sıkıştırılamadığını varsayar, sıfır ek sıkıştırma üst
   limiti. Bunların hiçbiri doğru değil, ancak etkiler küçük olacaktır.
Yönlendirici Bilgisinin diğer sıkıştırılabilir bölümlerini göz ardı eder.


## Spesifikasyon

Mevcut spesifikasyonlarımızda önerilen değişiklikler aşağıda belgelenmiştir.


### Ortak Yapılar
Ortak yapılar spesifikasyonunu değiştirme
Hedef açık anahtar alanının göz ardı edildiğini ve rastgele veriler içerebileceğini belirtin.

Ortak yapılar spesifikasyonuna Hedef açık anahtar alanı ve
Hedef ve Yönlendirici Kimliği'ndeki dolgu alanları için en iyi uygulamayı öneren bir bölüm ekleyin:

32 bayt rastgele veri oluşturmak için güçlü bir kriptografik sözde rastgele sayı üreteci (PRNG) kullanın
ve bu 32 baytı Hedef için açık anahtar alanını ve
Hedef ve Yönlendirici Kimliği için dolgu alanını dolduracak şekilde gerektiği kadar tekrarlayın.

### Özel Anahtar Dosyası
Özel anahtar dosyası (eepPriv.dat) formatı, spesifikasyonlarımızın resmi bir parçası değildir
ancak [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) belgelenmiştir ve diğer uygulamalar bunu destekler.
Bu, özel anahtarların farklı uygulamalara taşınabilirliğine olanak sağlar.
Bu javadocs'da şifreleme açık anahtarının rastgele dolgu olabileceğine ve şifreleme özel anahtarının tüm sıfır veya rastgele
veri olabileceğine dair bir not ekleyin.

### SAM
SAM spesifikasyonunda şifreleme özel anahtarının kullanılmadığını ve göz ardı edilebileceğini
belirtin. Herhangi bir rastgele veri istemci tarafından döndürülebilir.
SAM Köprüsü, Base 64 gösterimi bir dizi AAAA karakter içermemesi ve bozuk görünmemesi
için tüm sıfırlar yerine rastgele veriler gönderebilir (DEST GENERATE veya SESSION CREATE DESTINATION=TRANSIENT
ile oluşturma sırasında).


### I2CP
I2CP için değişiklik gerekmez. Hedefteki şifreleme açık anahtarı
ile ilişkili özel anahtar yönlendiriciye gönderilmez.


## Gelecek Planlama


### Protokol Değişiklikleri

Protokol değişiklikleri ve geriye dönük uyumluluk eksikliği maliyetine karşın,
Hedefteki, Yönlendirici Kimliğindeki veya her ikisinde dolgu alanını
ortadan kaldırmak için protokollerimizi ve spesifikasyonlarımızı değiştirebiliriz.

Bu öneri, sadece bir anahtar ve bir tür alanı içeren "b33" şifreli kiralama seti
formatına benzerdir.

Bazı protokol katmanları arasında biraz uyum korumak için dolgu alanı 
tüm sıfırlarla "genişletilebilir" ve diğer protokol katmanlarına
sunulabilir.

Hedefler için, anahtar sertifikasındaki şifreleme türü alanını iki bayt tasarruf sağlamak amacıyla 
kaldırabiliriz. Alternatif olarak, Hedefler anahtar sertifikasında bir sıfır
açık anahtar (ve dolgu) belirten yeni bir şifreleme türü 
alabilir.

Eğer geriye dönük uyumlu bir dönüştürme belirtilmez ise, aşağıdaki spesifikasyonlar, API'ler,
protokoller ve uygulamalar etkilenir:

- Ortak yapılar spesifikasyonu
- I2NP
- I2CP
- NTCP2
- SSU2
- Ratchet
- Akış
- SAM
- Bittorrent
- Yeniden tohumlama
- Özel Anahtar Dosyası
- Java çekirdeği ve yönlendirici API'si
- i2pd API'si
- Üçüncü taraf SAM kütüphaneleri
- Paketlenmiş ve üçüncü taraf araçlar
- Birkaç Java eklentisi
- Kullanıcı arayüzleri
- P2P uygulamaları örneğin MuWire, bitcoin, monero
- hosts.txt, adres defteri ve abonelikler

Eğer dönüşüm belirli bir katta belirtilirse, liste azaltılacaktır.

Bu değişikliklerin maliyetleri ve faydaları açık değildir.

Spesifik öneriler TBD:


### PQ Anahtarları

Post-Kuantum (PQ) şifreleme açık anahtarları, öngörülen herhangi bir algoritma
için, 256 bayttan büyüktür. Bu Yönlendirici Kimlikleri için tüm dolguyu ortadan kaldırır ve
yukarıda önerilen değişikliklerden elde edilen herhangi bir tasarrufu ortadan kaldırır.

"Hybrid" PQ yaklaşımında, SSL'nin yaptığı gibi, PQ anahtarları sadece efemerik olacaktır
ve Yönlendirici Kimliğinde görünmeyecektir.

PQ imza anahtarları uygulanabilir değildir ve Hedefler şifreleme açık anahtarlarını içermezler.
Ratchet için statik anahtarlar Kiralama Setindedir, Hedefte değil.
bu nedenle Hedefleri aşağıdaki tartışmadan eleme şansımız var.

Böylece PQ yalnızca Yönlendirici Bilgilerini etkiler ve sadece PQ statik (efemerik değil)
anahtarlar için, PQ hibrit için değil.
Bu, yeni bir şifreleme türü olur ve NTCP2, SSU2 ve şifrelenmiş Veri Tabanı Arama Mesajları ile
yanıtlarını etkiler.
Bu tasarım, geliştirme ve yayılma için öngörülen zaman çerçevesi nedir ????????
Ancak hibrit veya ratchetten sonra olur ????????????

Daha fazla tartışma için bkz [this topic](http://zzz.i2p/topics/3294).


## Sorunlar

Ağ için kaplama sağlamak amacıyla yavaş bir hızda yeniden anahtarlama yapmak
arzu edilebilir. "Yeniden anahtarlama" yalnızca dolguyu değiştirmek anlamına gelebilir, 
anahtarları gerçekten değiştirmek değil.

Mevcut hedeflerde yeniden anahtarlama mümkün değildir.

Açık anahtar alanında dolgu olan Yönlendirici Kimlikleri anahtar sertifikasında farklı 
bir şifreleme türü ile tanımlanmalı mı? Bu, uyumluluk sorunlarına neden olacaktır.


## Geçiş

Dolgu ile ElGamal anahtarını değiştirmek için geriye dönük uyumluluk sorunu yok.

Eğer uygulanırsa, yeniden anahtarlama
üç önceki yönlendirici kimlik geçişinde yapıldığı gibi olur:
DSA-SHA1 imzalarından ECDSA imzalarına, ardından
EdDSA imzalarına, ardından X25519 şifreleme.

Geriye dönük uyumluluk sorunlarına tabi olarak, ve SSU devre dışı bırakıldıktan sonra,
uygulamalar ElGamal kodunu tamamen kaldırabilir.
Ağdaki yönlendiricilerin yaklaşık %14'ü ElGamal şifreleme türündedir, bunların birçoğu floodfill'dir.

Java I2P için bir taslak birleştirme isteği [git.idk.i2p](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/merge_requests/66) adresindedir.
