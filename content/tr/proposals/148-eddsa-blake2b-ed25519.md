---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Open"
thread: "http://zzz.i2p/topics/2689"
---

## Genel Bakış

Bu öneri, SHA-512 yerine
kişiselleştirme dizgileri ve tuzlar ile birlikte BLAKE2b-512 kullanan yeni bir imza türü eklemektedir.
Bu, üç türdeki potansiyel saldırıyı ortadan kaldıracaktır.

## Motivasyon

NTCP2 (öneri 111) ve LS2 (öneri 123) tasarımı ve tartışmaları sırasında,
çeşitli saldırıları ve bu saldırıların nasıl önlenebileceğini kısa bir süre düşündük.
Bu saldırılardan üçü Uzunluk Uzantısı Saldırıları, Protokoller Arası Saldırılar ve Çift Mesaj Tanımlamadır.

Hem NTCP2 hem de LS2 için, bu saldırıların mevcut önerilerle doğrudan ilgili olmadığını ve
herhangi bir çözümün yeni ilkelere karşı çeliştiğini belirledik.
Ayrıca, bu protokollerdeki karma işlevlerinin hızının kararlarımızda önemli bir
etken olmadığını belirledik.
Bu nedenle, çözümü ayrı bir öneriye erteledik.
LS2 spesifikasyonuna bazı kişiselleştirme özellikleri eklerken,
yeni karma işlevleri gerektirmedik.

ZCash gibi birçok proje [ZCASH]_,
yeni algoritmalara dayanan ve aşağıdaki saldırılara
karşı savunmasız olmayan karma işlevlerini ve imza algoritmalarını kullanmaktadır.

### Uzunluk Uzantısı Saldırıları

SHA-256 ve SHA-512 Uzunluk Uzantısı Saldırılarına (LEA) karşı savunmasızdır [LEA]_.
Bu, gerçek verilerin değil, verinin karmasının imzalandığı durumlarda geçerlidir.
Çoğu I2P protokolünde (akış, veri akışı, netdb ve diğerleri), gerçek veriler imzalanır.
Bir istisna, karmanın imzalandığı SU3 dosyalarıdır.
Diğer bir istisna, yalnızca DSA için imzalanmış veri akışları (imza türü 0) olup,
bu durumda karma imzalanır.
Diğer imzalı veri akış türleri için, veri imzalanır.

### Protokoller Arası Saldırılar

I2P protokollerindeki imzalı veriler,
alan ayrımı eksikliğinden dolayı Protokoller Arası Saldırılara (CPA) karşı savunmasız olabilir.
Bu durum, bir saldırganın bir bağlamda (örneğin imzalı bir veri akışı)
alınan veriyi başka bir bağlamda (örneğin akış veya ağ veritabanı) geçerli,
imzalı veri olarak sunmasına olanak tanır.
Bir bağlamdaki imzalı verinin başka bir bağlamda
geçerli veri olarak ayrıştırılması olası olmasa da,
tüm durumları kesin olarak analiz etmek zordur veya imkansızdır.
Ayrıca, bir bağlamda, bir saldırganın kurbanı başka bir bağlamda
geçerli veri olabilecek özel olarak hazırlanmış verileri
imzalamaya zorlayabilmesi mümkün olabilir.
Yine, tüm durumları kesin olarak analiz etmek zordur veya imkansızdır.

### Çift Mesaj Tanımlama

I2P protokolleri, Çift Mesaj Tanımlama (DMI) saldırısına karşı savunmasız olabilir.
Bu, bir saldırganın iki imzalı mesajın aynı içeriğe sahip olduğunu
tanımlamasına olanak tanıyabilir; bu mesajlar ve imzaları şifrelenmiş olsa bile.
I2P'de kullanılan şifreleme yöntemleri nedeniyle bu durum olası değilse de,
tüm durumları kesin olarak analiz etmek zordur veya imkansızdır.
Bir rastgele tuz ekleme yöntemi sağlayan bir karma işlevi kullanarak,
aynı verileri imzalarken tüm imzalar farklı olacaktır.
Öneri 123'te tanımlandığı gibi Red25519 karma işlevine
rastgele bir tuz eklese de, bu sorun şifrelenmemiş kiralama setleri için
çözülmez.

### Hız

Bu öneri için birincil bir motivasyon olmasa da,
SHA-512 nispeten yavaştır ve mevcut daha hızlı karma işlevleri vardır.

## Hedefler

- Yukarıdaki saldırıları önlemek
- Yeni kripto ilkel kullanımlarını minimize etmek
- Kanıtlanmış, standart kripto ilkel kullanmak
- Standart eğrileri kullanmak
- Mevcutsa daha hızlı ilkel kullanmak

## Tasarım

Mevcut RedDSA_SHA512_Ed25519 imza türünü
SHA-512 yerine BLAKE2b-512 ile değiştirilmesi.
Her kullanım durumu için benzersiz kişiselleştirme dizgileri ekleyin.
Yeni imza türü, hem kör olmayan hem de kör kiralama setleri için kullanılabilir.

## Gerekçelendirme

- BLAKE2b, LEA'ya karşı savunmasız değildir [BLAKE2]_.
- BLAKE2b, alan ayrımı için kişiselleştirme dizgileri eklemek için standart bir yol sağlar.
- BLAKE2b, DMI'yı önlemek için rastgele bir tuz eklemek için standart bir yol sağlar.
- BLAKE2b, modern donanımda SHA-256 ve SHA-512'den (ve MD5'ten) daha hızlıdır,
  [BLAKE2]'ye göre.
- Ed25519, Java'da en azından ECDSA'dan daha hızlı olan en hızlı imza türümüzdür.
- Ed25519 [ED25519-REFS]_ 512 bitlik bir kriptografik karma işlev gerektirir.
  SHA-512'yi belirtmez. BLAKE2b de hash işlevi için uygundur.
- BLAKE2b, Noise gibi birçok programlama dili kütüphanesinde yaygın olarak bulunabilir.

## Spesifikasyon

Tuz ve kişiselleştirme ile [BLAKE2]'deki gibi anahtarsız BLAKE2b-512 kullanılacaktır.
BLAKE2b imzalarının tüm kullanımları 16 karakterlik bir kişiselleştirme dizgisi kullanacaktır.

RedDSA_BLAKE2b_Ed25519 imzalamada kullanıldığında,
rastgele bir tuz kullanmak mümkündür, ancak gerekli değildir, çünkü imza algoritması
80 bayt rastgele veri ekler (öneri 123'e bakın).
İstenirse, r hesaplamak için veriyi karma yaparken,
her imza için yeni bir BLAKE2b 16 bayt rastgele tuz ayarlayın.
S'yi hesaplarken tuzu sıfır tüm'e ayarlayın.

RedDSA_BLAKE2b_Ed25519 doğrulamada kullanıldığında,
rastgele bir tuz kullanmayın, sıfır tüm deyimine ayarlayın.

Tuz ve kişiselleştirme özellikleri [RFC-7693]'de belirtilmemiştir;
bu özellikleri [BLAKE2]'te belirtildiği gibi kullanın.

### İmza Türü

RedDSA_BLAKE2b_Ed25519 için, RedDSA_SHA512_Ed25519 (öneri 123'te tanımlandığı gibi imza türü 11)
SHA-512 karma işlevini BLAKE2b-512 ile değiştirin. Başka değişiklik yok.

su3 dosyaları için EdDSA_SHA512_Ed25519ph (imza türü 8) için
bir yedeğe ihtiyaç duymuyoruz, çünkü EdDSA'nın ön karmalı versiyonu LEA'ya karşı savunmasız değildir.
EdDSA_SHA512_Ed25519 (imza türü 7) su3 dosyaları için desteklenmez.

=======================  ===========  ======  =====
        Type             Type Code    Since   Usage
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        TBD    Yönlendirici Kimlikleri, Hedefler ve şifrelenmiş kiralama setleri için yalnızca; Yönlendirici Kimlikleri için asla kullanılmaz
=======================  ===========  ======  =====

### Ortak Yapı Veri Uzunlukları

Aşağıdakiler yeni imza türü için geçerlidir.

==================================  =============
            Veri Türü              Uzunluk    
==================================  =============
Karma                                 64      
Özel Anahtar                          32      
Açık Anahtar                          32      
İmza                                  64      
==================================  =============

### Kişiselleştirmeler

İmzaların çeşitli kullanımları için alan ayrımı sağlamak amacıyla,
BLAKE2b kişiselleştirme özelliğini kullanacağız.

BLAKE2b imzalarının tüm kullanımları 16 karakterlik bir kişiselleştirme dizgisi kullanacaktır.
Herhangi bir yeni kullanım, benzersiz bir kişiselleştirme ile burada tabloya eklenmelidir.

NTCP 1 ve SSU el sıkışması, el sıkışmasında tanımlandığı gibi imzalanmış veriler içindir.
DatabaseStore Mesajlarındaki imzalı RouterInfos, NetDB Girişi kişiselleştirmesi kullanacaktır,
tıpkı NetDB'de saklanıyormuş gibi.

==================================  ==========================
         Kullanım                  16 Bayt Kişiselleştirme
==================================  ==========================
I2CP SessionConfig                  "I2CP_SessionConf"
NetDB Girişleri (RI, LS, LS2)      "network_database"
NTCP 1 el sıkışma                   "NTCP_1_handshake"
İmzalanmış Veri Akışları            "sign_datagramI2P"
Akış                                "streaming_i2psig"
SSU el sıkışma                      "SSUHandshakeSign"
SU3 Dosyaları                       n/a, desteklenmez
Birim Testleri                      "test1234test5678"
==================================  ==========================

## Notlar

## Sorunlar

- Alternatif 1: Öneri 146;
  LEA direnci sağlar
- Alternatif 2: Ed25519ctx RFC 8032'de;
  LEA direnci ve kişiselleştirme sağlar.
  Standartlaştırılmış, ancak herhangi biri kullanıyor mu?
  Bkz. [RFC-8032]_ ve [ED25519CTX]_.
- "Anahtarlı" karmaşalama bizim için faydalı mı?

## Geçiş

Önceki imza türleri için uygulananleştirmede olduğu gibi.

Varsayılan olarak yeni yönlendiricilerde türü 7'den tür 12'ye değiştirmeyi planlıyoruz.
Varsayılan olarak tür 7'den tür 12'ye mevcut yönlendiricileri sonunda taşımayı planlıyoruz,
tür 7 tanıtıldıktan sonra kullanılan "anahtar değişim" sürecini kullanarak.
Varsayılan olarak yeni hedeflerde tür 7'den tür 12'ye değiştirmeyi planlıyoruz.
Varsayılan olarak yeni şifrelenmiş hedeflerde tür 11'den tür 13'e değiştirmeyi planlıyoruz.

Türler 7, 11 ve 12'den tür 12'ye körleme desteği sağlayacağız.
Tür 12'yi tür 11'e körleme desteği sağlamayacağız.

Yeni yönlendiriciler birkaç ay sonra varsayılan olarak yeni imza türünü kullanabilir.
Yeni hedefler, belki bir yıl sonra varsayılan olarak yeni imza türünü kullanabilir.

Minimum yönlendirici sürümü 0.9.TBD için, yönlendiriciler aşağıdaki noktaları sağlamalıdır:

- 0.9.TBD versiyonundan daha düşük versiyonlardaki yönlendiricilere yeni imza türü içeren bir RI veya LS depolamayın (veya tümleştirmeyin).
- netdb deposunu doğrularken, 0.9.TBD versiyonundan daha düşük yönlendiricilerden yeni imza türü ile bir RI veya LS almayın.
- RI'ında yeni imza türü olan yönlendiriciler, 0.9.TBD versiyonundan daha düşük yönlendiricilere NTCP, NTCP2 veya SSU ile bağlantı kuramayabilir.
- Akış bağlantıları ve imzalı veri akışları 0.9.TBD versiyonundan daha düşük yönlendiriciler için çalışmayabilir,
  ancak bunu bilmenin bir yolu yoktur, bu yüzden 0.9.TBD yayınlandıktan sonra varsayılan olarak yeni imza türünün birkaç ay veya yıl boyunca kullanılmaması gerekir.

## Kaynaklar

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "Yüksek hızda yüksek güvenlik imzaları" Daniel
    J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe ve
    Bo-Yin Yang tarafından. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://tr.wikipedia.org/wiki/Length_extension_attack

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
