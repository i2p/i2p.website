---
title: "Düşük Seviye Kriptografi Spesifikasyonu"
description: "I2P'de kullanılan kriptografik algoritmaların düşük seviye ayrıntıları"
slug: "cryptography"
aliases:
  - "/tr/how_cryptography"
  - "/tr/how_cryptography/"
category: "Tasarım"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Genel Bakış

> **Not:** Bu belge büyük ölçüde güncelliğini yitirmiştir. Güncel spesifikasyonlar için aşağıdaki belgelere bakınız: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Bu sayfa I2P'deki kriptografinin düşük seviye detaylarını belirtir.

I2P içinde kullanılmakta olan birkaç kriptografik algoritma bulunmaktadır. I2P'nin orijinal tasarımında, her türden yalnızca bir tane vardı - bir simetrik algoritma, bir asimetrik algoritma, bir imzalama algoritması ve bir hash algoritması. Daha fazla algoritma ekleme veya daha güvenli olanlara geçiş yapma için herhangi bir hüküm yoktu.

Son yıllarda, geriye dönük uyumlu bir şekilde birden fazla temel işlemi ve kombinasyonu desteklemek için bir çerçeve ekledik. Değişen anahtar ve imza uzunluklarına sahip çok sayıda imza algoritması, "imza türleri" ile tanımlanmaktadır. Asimetrik ve simetrik şifreleme kombinasyonu kullanan ve değişen anahtar uzunluklarına sahip uçtan uca şifreleme şemaları, "şifreleme türleri" ile tanımlanmaktadır.

I2P'deki çeşitli protokoller ve veri yapıları, imza türünü ve/veya şifreleme türünü belirtmek için alanlar içerir. Bu alanlar, tür tanımlarıyla birlikte, anahtar ve imza uzunluklarını ve bunları kullanmak için gereken kriptografik temel öğeleri tanımlar. İmza ve şifreleme türlerinin tanımları [Ortak Yapılar spesifikasyonunda](/docs/specs/common-structures) yer almaktadır.

Orijinal I2P protokolleri NTCP, SSU ve ElGamal/AES+SessionTags, ElGamal asimetrik şifreleme ve AES simetrik şifrelemenin bir kombinasyonunu kullanır. Daha yeni protokoller NTCP2 ve ECIES-X25519-AEAD-Ratchet, X25519 anahtar değişimi ve ChaCha20/Poly1305 simetrik şifrelemenin bir kombinasyonunu kullanır.

- ECIES-X25519-AEAD-Ratchet, ElGamal/AES+SessionTags'i değiştirdi.
- NTCP2, NTCP'yi değiştirdi.
- SSU2, SSU'yu değiştirdi.
- X25519 tunnel oluşturma, ElGamal tunnel oluşturmayı değiştirdi.

## Asimetrik Şifreleme

I2P'de orijinal asimetrik şifreleme algoritması ElGamal'dir. Çeşitli yerlerde kullanılan daha yeni algoritma ise ECIES X25519 DH anahtar değişimi'dir.

Tüm ElGamal kullanımını X25519'a taşıma sürecindeyiz.

NTCP (ElGamal ile) NTCP2'ye (X25519 ile) taşındı. ElGamal/AES+SessionTag, ECIES-X25519-AEAD-Ratchet'e taşınmakta.

### X25519

X25519 kullanımının ayrıntıları için [NTCP2](/docs/specs/ntcp2) ve [ECIES](/docs/specs/ecies) belgelerine bakın.

### ElGamal

ElGamal, I2P'de çeşitli yerlerde kullanılır:

- Router'dan router'a TunnelBuild mesajlarını şifrelemek için
- LeaseSet içindeki şifreleme anahtarını kullanan ElGamal/AES+SessionTag'in bir parçası olarak uçtan uca (hedeften hedefe) şifreleme için
- ElGamal/AES+SessionTag'in bir parçası olarak floodfill router'lara gönderilen bazı netDb depolama ve sorgularının şifrelenmesi için (hedeften router'a veya router'dan router'a).

2048 bit ElGamal şifreleme ve şifre çözme için IETF [RFC-3526](http://tools.ietf.org/html/rfc3526) tarafından verilen ortak asal sayıları kullanıyoruz. Şu anda ElGamal'ı yalnızca tek bir blokta IV ve oturum anahtarını şifrelemek için kullanıyoruz, ardından bu anahtar ve IV kullanılarak AES şifrelenmiş yük verisi takip ediyor.

Şifrelenmemiş ElGamal şunları içerir:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data), ElGamal bloğunda şifrelenen verinin SHA256'sıdır ve önünde rastgele sıfır olmayan bir bayt bulunur. Bu bayt 0.9.28 sürümü itibariyle gerçekten rastgeledir; bundan önce her zaman 0xFF idi. Gelecekte bayraklar için kullanılabilir. Blokta şifrelenen veri en fazla 222 bayt uzunluğunda olabilir. Düz metin 222 baytten küçükse şifrelenmiş veri önemli miktarda sıfır içerebileceğinden, üst katmanların düz metni rastgele verilerle 222 bayta doldurması önerilir. Toplam uzunluk: genellikle 255 bayt.

Şifrelenmiş ElGamal şunları içerir:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Her şifrelenmiş bölüm, tam olarak 257 bayt boyutuna ulaşması için başına sıfırlar eklenir. Toplam uzunluk: 514 bayt. Tipik kullanımda, üst katmanlar açık metin verilerini 222 bayta doldurur ve bu da 255 baytlık şifrelenmemiş bir blok oluşturur. Bu, iki adet 256 baytlık şifrelenmiş bölüm olarak kodlanır ve bu katmanda her bölümden önce tek baytlık sıfır dolgusu bulunur.

ElGamal kodunu görmek için [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

Paylaşılan asal sayı, 2048 bit anahtarlar için Oakley asal sayısıdır [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
veya onaltılık değer olarak:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Generator olarak 2 kullanılıyor.

#### Kısa Üs {#exponent}

Standart üs boyutu 2048 bit (256 bayt) ve I2P PrivateKey tam 256 bayt olsa da, bazı durumlarda 226 bitlik (28.25 bayt) kısa üs boyutunu kullanırız. Bu, Oakley asal sayıları ile kullanım için güvenli olmalıdır [vanOorschot1996] [BENCHMARKS].

Ayrıca, [Koshiba2004] bu sci.crypt dizisine göre [SCI.CRYPT] bunu destekliyor gibi görünüyor. PrivateKey'in geri kalanı sıfırlarla doldurulur.

Sürüm 0.9.8'den önce, tüm router'lar kısa üssü kullanıyordu. Sürüm 0.9.8 itibariyle, 64-bit x86 router'lar tam 2048-bit üs kullanmaktadır. Artık tüm router'lar tam üssü kullanmaktadır, işlemci yükü endişeleri nedeniyle kısa üssü kullanmaya devam eden çok yavaş donanımlardaki az sayıdaki router hariç. Bu platformlar için daha uzun üsse geçiş, daha fazla araştırma gerektiren bir konudur.

#### Eskime

Ağın ElGamal saldırısına karşı güvenlik açığı ve daha uzun bit uzunluğuna geçişin etkisi incelenecektir. Herhangi bir değişikliği geriye dönük uyumlu hale getirmek oldukça zor olabilir.

## Simetrik Şifreleme

I2P'deki orijinal simetrik şifreleme algoritması AES'tir. Çeşitli yerlerde kullanılan daha yeni algoritma ise Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305'tir.

Tüm AES kullanımını ChaCha20/Poly1305'e geçirme sürecindeyiz.

NTCP (AES ile) NTCP2'ye (ChaCha20/Poly1305 ile) geçirildi. ElGamal/AES+SessionTag, ECIES-X25519-AEAD-Ratchet'e geçiriliyor.

### ChaCha20/Poly1305

ChaCha20/Poly1305 kullanımının detayları için [NTCP2](/docs/specs/ntcp2) ve [ECIES](/docs/specs/ecies) bölümlerine bakınız.

### AES

AES simetrik şifreleme için çeşitli durumlarda kullanılır:

- DH anahtar değişiminden sonra SSU transport şifrelemesi için ("Transports" bölümüne bakın)
- ElGamal/AES+SessionTag'in bir parçası olarak uçtan uca (destination-to-destination) şifreleme için
- ElGamal/AES+SessionTag'in bir parçası olarak floodfill router'lara gönderilen bazı netDb store ve sorgu işlemlerinin şifrelemesi için (destination-to-router veya router-to-router).
- Router'ın kendi tunnel'ları üzerinden kendisine gönderdiği periyodik tunnel test mesajlarının şifrelemesi için.

CBC modunda 256 bit anahtarlar ve 128 bit bloklar ile AES kullanıyoruz. Kullanılan dolgu IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, bölüm 8.1 (blok tipi 02 için)) standardında belirtilmiştir. Bu durumda, dolgu 16 baytlık blokları eşleştirmek için sözde rastgele üretilen oktetlerden oluşur. Özellikle CBC kodu [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) ve Cryptix AES uygulaması [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java) ile ElGamalAESEngine.getPadding fonksiyonunda bulunan dolgu [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java) kodlarını inceleyin.

#### Eskime

Ağın AES saldırısına karşı güvenlik açığı ve daha uzun bit uzunluğuna geçişin etkisi incelenecektir. Herhangi bir değişikliği geriye dönük uyumlu hale getirmek oldukça zor olabilir.

## İmzalar {#sig}

Çok sayıda imza algoritması, değişken anahtar ve imza uzunlukları ile imza türleri tarafından tanımlanır. Daha fazla imza türü eklemek nispeten kolaydır.

EdDSA-SHA512-Ed25519 mevcut varsayılan imza algoritmasıdır. İmza türleri desteği eklemeden önce kullanılan orijinal algoritma olan DSA, hala ağda kullanılmaktadır.

### DSA

İmzalar, [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java) içinde uygulandığı şekliyle 1024 bit [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) (L=1024, N=160) ile oluşturulur ve doğrulanır. DSA, imzalar için ElGamal'dan çok daha hızlı olduğu için tercih edilmiştir.

#### SEED

160 bit:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Sayaç

```
33
```
#### DSA asalı (p)

1024 bit:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA bölümü (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA üreteci (g)

1024 bit:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey 1024 bittir. SigningPrivateKey 160 bittir.

#### Eskime

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) 2010 sonrası kullanım için minimum (L=2048, N=224) önerir. Bu, belirli bir anahtarın "kripto periyodu" veya yaşam süresi ile bir ölçüde azaltılabilir.

Asal sayı 2003 yılında seçildi ve bu sayıyı seçen kişi (TheCrypto) şu anda artık bir I2P geliştiricisi değil. Bu nedenle, seçilen asal sayının 'güçlü bir asal sayı' olup olmadığını bilmiyoruz. Gelecekteki amaçlar için daha büyük bir asal sayı seçilirse, bunun güçlü bir asal sayı olması gerekir ve yapım sürecini belgeleyeceğiz.

## Yeni İmza Algoritmaları

0.9.12 sürümünden itibaren, router 1024-bit DSA'dan daha güvenli olan ek imza algoritmalarını desteklemektedir. İlk kullanım Destinations için olmuştur; Router Identities desteği 0.9.16 sürümünde eklenmiştir. Mevcut Destinations eski imzalardan yeni imzalara geçirilemez; ancak, birden fazla Destinations ile tek tunnel desteği bulunmaktadır ve bu yeni imza türlerine geçiş için bir yol sağlamaktadır. İmza türü Destination ve Router Identity içinde kodlandığından, yeni imza algoritmaları veya eğrileri herhangi bir zamanda eklenebilir.

Şu anda desteklenen imza türleri aşağıdaki gibidir:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (yaygın olarak kullanılmaz)
- ECDSA-SHA512-P521 (yaygın olarak kullanılmaz)
- EdDSA-SHA512-Ed25519 (0.9.15 sürümünden itibaren varsayılan)
- RedDSA-SHA512-Ed25519 (0.9.39 sürümünden itibaren)

Ek imza türleri yalnızca uygulama katmanında kullanılır, öncelikli olarak su3 dosyalarını imzalamak ve doğrulamak için. Bu imza türleri şu şekildedir:

- RSA-SHA256-2048 (yaygın olarak kullanılmaz)
- RSA-SHA384-3072 (yaygın olarak kullanılmaz)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (0.9.25 sürümünden itibaren; yaygın olarak kullanılmaz)

### ECDSA

ECDSA standart NIST eğrilerini ve standart SHA-2 hash'lerini kullanır.

Yeni hedefleri 0.9.16 - 0.9.19 sürüm zaman diliminde ECDSA-SHA256-P256'ya taşıdık. Router Kimlikler için kullanım 0.9.16 sürümünden itibaren desteklenmekte ve mevcut router'ların taşınması 2015'te gerçekleşti.

### RSA

Standart RSA PKCS#1 v1.5 (RFC 2313) F4 = 65537 public üssü ile.

RSA artık router güncellemeleri, reseeding, eklentiler ve haberler dahil olmak üzere tüm bant dışı güvenilir içeriği imzalamak için kullanılmaktadır. İmzalar "su3" formatına [UPDATES] gömülüdür. 4096-bit anahtarlar önerilir ve bilinen tüm imzalayıcılar tarafından kullanılır. RSA, ağ içi Destination'larda veya Router Identity'lerde kullanılmaz veya kullanılması planlanmaz.

### EdDSA 25519

Curve 25519 ve standart 512-bit SHA-2 hash'leri kullanan standart EdDSA.

0.9.15 sürümünden itibaren desteklenmektedir.

Hedefler ve Router Kimlikleri 2015'in sonlarında geçirildi.

### RedDSA 25519

Curve 25519 ve standart 512-bit SHA-2 hash'leri kullanan standart EdDSA, ancak farklı özel anahtarlar ve imzalamaya küçük değişiklikler ile. Şifreli leaseSet'ler için. Detaylar için [EncryptedLeaseSet](/docs/specs/encryptedleaseset) ve [Red25519](/docs/specs/red25519) bölümlerine bakın.

0.9.39 sürümünden itibaren desteklenmektedir.

## Hash'ler

Hash'ler imza algoritmalarında ve ağın DHT'sinde anahtar olarak kullanılır.

Eski imza algoritmaları SHA1 ve SHA256 kullanır. Yeni imza algoritmaları SHA512 kullanır. DHT, SHA256 kullanır.

### SHA256

I2P içindeki DHT hash'leri standart SHA256'dır.

#### Eskime

Ağın SHA-256 saldırısına karşı güvenlik açığı ve daha uzun bir hash'e geçişin etkisi incelenmelidir. Herhangi bir değişikliği geriye dönük uyumlu hale getirmek oldukça zor olabilir.

## Aktarım Protokolleri

En alt protokol katmanında, router'lar arası noktadan noktaya iletişim, aktarım katmanı güvenliği ile korunmaktadır.

NTCP2 bağlantıları X25519 Diffie-Hellman ve ChaCha20/Poly1305 kimlik doğrulamalı şifreleme kullanır.

SSU ve kullanımdan kaldırılan NTCP aktarımları, yukarıda ElGamal için belirtilen aynı paylaşılan asal sayı ve üreteci kullanan 256 bayt (2048 bit) Diffie-Hellman anahtar değişimi kullanır ve ardından yukarıda açıklandığı gibi simetrik AES şifreleme uygular.

SSU'nun SSU2'ye (X25519 ve ChaCha20/Poly1305 ile) geçirilmesi planlanmaktadır.

Tüm taşıma katmanları, taşıma bağlantılarında mükemmel ileri gizlilik [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) sağlar.

### NTCP2 bağlantıları {#tcp}

NTCP2 bağlantıları X25519 Diffie-Hellman ve ChaCha20/Poly1305 kimlik doğrulamalı şifreleme ile Noise protokol çerçevesi [Noise](https://noiseprotocol.org/noise.html) kullanır.

Ayrıntılar ve referanslar için NTCP2 spesifikasyonuna [NTCP2](/docs/specs/ntcp2) bakın.

### UDP bağlantıları {#udp}

SSU (UDP taşıma katmanı), 2048 bit Diffie-Hellman değişimi yoluyla geçici oturum anahtarı üzerinde anlaştıktan, diğer router'ın DSA anahtarı ile istasyondan istasyona kimlik doğrulaması yaptıktan sonra her paketi hem açık IV hem de MAC (HMAC-MD5-128) ile AES256/CBC kullanarak şifreler, ayrıca her ağ mesajının yerel bütünlük kontrolü için kendi hash'i vardır.

Ayrıntılar için SSU spesifikasyonuna bakın.

UYARI - I2P'nin SSU'da kullandığı HMAC-MD5-128 görünüşe göre standart dışıdır. Görünüşe göre, SSU'nun erken bir sürümü HMAC-SHA256 kullanıyordu ve daha sonra performans nedenleriyle MD5-128'e geçildi, ancak 32-byte buffer boyutu değiştirilmeden bırakıldı. Ayrıntılar için HMACGenerator.java ve 2005-07-05 durum notlarına bakın.

### NTCP bağlantıları

NTCP artık kullanılmıyor, yerini NTCP2 aldı.

NTCP bağlantıları, router'ın kimliğini kullanarak istasyondan istasyona anlaşması ile devam eden 2048 Diffie-Hellman uygulaması ile müzakere edildi, ardından bazı şifrelenmiş protokol özel alanları geldi ve sonraki tüm veriler AES ile şifrelendi (yukarıda belirtildiği gibi). ElGamalAES+SessionTag kullanmak yerine DH müzakeresini yapmanın temel nedeni, '(mükemmel) ileri gizlilik' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) sağlamasıdır, ElGamalAES+SessionTag ise bunu sağlamaz.

## Kaynaklar

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Crypto++ kıyaslamaları, aslen http://www.eskimo.com/~weidai/benchmarks.html adresindeydi (artık ölü), http://www.archive.org/ adresinden kurtarıldı, 23 Nisan 2008 tarihli.
- [Common](/docs/specs/common-structures) - Ortak Yapılar Spesifikasyonu
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
