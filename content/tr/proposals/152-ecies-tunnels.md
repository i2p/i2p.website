---
title: "ECIES Tünelleri"
number: "152"
author: "chisana, zzz, orjinal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
---

## Not
Ağ dağıtımı ve testi devam ediyor.
Küçük revizyonlar yapılabilir.
Resmi spesifikasyon için [SPEC](/en/docs/spec/) adresine bakın.


## Genel Bakış

Bu belge, [ECIES-X25519](/en/docs/spec/ecies/) tarafından tanıtılan kripto ilkeleri kullanarak Tünel Oluşturma mesajı şifrelemesinde değişiklikler önermektedir.
Bu, yönlendiricileri ElGamal'dan ECIES-X25519 anahtarlarına dönüştürme önerisinin bir parçasıdır [Prop156](/en/proposals/156-ecies-routers/).

Ağın ElGamal + AES256'dan ECIES + ChaCha20'ya geçişi için,
karışık ElGamal ve ECIES yönlendiricileri olan tüneller gereklidir.
Karışık tünel atlamalarının nasıl ele alınacağına dair spesifikasyonlar sağlanmıştır.
ElGamal atlamalarının formatı, işleme veya şifrelemesinde herhangi bir değişiklik yapılmayacak.

ElGamal tünel oluşturucuları, her atlama başına geçici X25519 anahtar çiftleri oluşturmalı ve
ECIES atlamaları içeren tünel oluşturmak için bu standardı takip etmelidir.

Bu öneri, ECIES-X25519 Tünel Oluşturma için gereken değişiklikleri belirtir.
ECIES yönlendiricileri için gerekli tüm değişikliklerin genel bir görünümü için, öneri 156'ya [Prop156](/en/proposals/156-ecies-routers/) bakın.

Bu öneri, uyumluluk için tünel oluşturma kayıtlarının aynı boyutta kalmasını sağlar. Daha küçük oluşturma kayıtları ve mesajlar
daha sonra uygulanacaktır - bkz. [Prop157](/en/proposals/157-new-tbm/).


### Kriptografik İkinciller

Yeni kriptografik ikinciller tanıtılmamıştır. Bu öneriyi uygulamak için gereken ikinciller:

- [Cryptography](/en/docs/spec/cryptography/) içinde olduğu gibi AES-256-CBC
- STREAM ChaCha20/Poly1305 fonksiyonları:
  ENCRYPT(k, n, plaintext, ad) ve DECRYPT(k, n, ciphertext, ad) - [NTCP2](/en/docs/spec/ntcp2/) [ECIES-X25519](/en/docs/spec/ecies/) ve [RFC-7539](https://tools.ietf.org/html/rfc7539) içinde olduğu gibi
- [NTCP2](/en/docs/spec/ntcp2/) ve [ECIES-X25519](/en/docs/spec/ecies/) içinde olduğu gibi X25519 DH fonksiyonları
- HKDF(salt, ikm, info, n) - [NTCP2](/en/docs/spec/ntcp2/) ve [ECIES-X25519](/en/docs/spec/ecies/) içinde olduğu gibi

Başka yerlerde tanımlanmış Noise fonksiyonları:

- MixHash(d) - [NTCP2](/en/docs/spec/ntcp2/) ve [ECIES-X25519](/en/docs/spec/ecies/) içinde olduğu gibi
- MixKey(d) - [NTCP2](/en/docs/spec/ntcp2/) ve [ECIES-X25519](/en/docs/spec/ecies/) içinde olduğu gibi


### Hedefler

- Kripto işlemlerinin hızını artırmak
- ElGamal + AES256/CBC'yi Tünel BuildRequestRecords ve BuildReplyRecords için ECIES ikincilleriyle değiştirmek.
- Şifrelenmiş BuildRequestRecords ve BuildReplyRecords boyutunda değişiklik yapılmaması (528 byte) uyumluluk için
- Yeni I2NP mesajı yok
- Uyumluluk için şifrelenmiş oluşturma kayıt boyutunu koruma
- Tünel Oluşturma Mesajları için iletim gizliliği ekleme.
- Kimlik doğrulamalı şifreleme ekleme
- BuildRequestRecords'taki sıralama atlamalarını algılama
- Bloom filtresi boyutunun azaltılabilmesi için zaman damgasının çözünürlüğünü artırma
- Değişken tünel ömürlerinin mümkün olabilmesi için tünel bitiş alanı ekleme (sadece ECIES tünelleri için)
- Gelecek özellikler için genişletilebilir seçenek alanı ekleme
- Mevcut kriptografik ikincillerin yine kullanımı
- Tünel oluşturma mesaj güvenliğini mümkün olduğunca iyileştirme ile birlikte uyumluluğu koruma
- Karışık ElGamal/ECIES eşleri ile tünelleri destekleme
- Oluşturma mesajları üzerinde "etiketleme" saldırılarına karşı korumaları iyileştirme
- Atlamaların, oluşturma mesajını işlemeye başlamadan önce bir sonraki atlamanın şifreleme türünü bilmeleri gerekmemektedir,
  çünkü o anda bir sonraki atlamanın RI bilgisine sahip olmayabilirler
- Mevcut ağ ile maksimum uyumluluk sağlanması
- ElGamal yönlendiriciler için tünel oluşturma AES istek/cevap şifrelemesinde değişiklik yapılmaması
- Tünel AES "katman" şifrelemesinde değişiklik yapılmaması, bu konuda [Prop153](/en/proposals/153-chacha20-layer-encryption/) adresine bakınız
- Hem 8 kayıtlı TBM/TBRM hem de değişken boyutlu VTBM/VTBRM'yi desteklemeye devam etme
- Tüm ağa bir "flag day" yükseltmesi gerektirmemesi


### Hedef Olmayanlar

- Bir "flag day" gerektiren tünel oluşturma mesajlarının tamamen yeniden tasarlanması.
- Tünel oluşturma mesajlarını küçültmek (tüm ECIES atlamalarını ve yeni bir öneri gerektirir)
- Sadece küçük mesajlar için gerekli olan [Prop143](/en/proposals/143-build-message-options/) tarafından tanımlanan tünel oluşturma seçeneklerinin kullanımı
- İki yönlü tüneller - bunun için bkz. [Prop119](/en/proposals/119-bidirectional-tunnels/)
- Daha küçük tünel oluşturma mesajları - bunun için bkz. [Prop157](/en/proposals/157-new-tbm/)


## Tehdit Modeli

### Tasarım Hedefleri

- Hiçbir atlama, tünelin başlatıcısını belirleyememelidir.

- Orta atlamalar, tünelin yönünü veya tüneldeki konumlarını belirleyememelidir.

- Hiçbir atlama, diğer istek veya yanıt kayıtlarının içeriğini, sonraki atlama için kesilmiş yönlendirici karması ve geçici anahtarı hariç okuyamaz.

- Dışa dönük yapı için yanıt tünelinin hiçbir üyesi yanıt kayıtlarını okuyamaz.

- İç yapı için dışa dönük tünelin hiçbir üyesi istek kayıtlarını okuyamaz, OBEP sadece kesilmiş yönlendirici karması ve IBGW için geçici anahtarı görebilir.


### Etiketleme Saldırıları

Tünel oluşturma tasarımının ana amacı, işbirliği içindeki yönlendiricilerin X ve Y'nin tek bir tünelde olduklarını bilmelerini zorlaştırmaktır.
Yönlendirici X hop m konumunda ve yönlendirici Y hop m+1 konumunda ise, bunu açıkça bileceklerdir.
Ancak yönlendirici X hop m konumunda ve yönlendirici Y hop m+n konumunda ise (n>1 için), bu çok daha zor olmalıdır.

Etiketleme saldırıları, orta-hop yönlendirici X'in tünel oluşturma mesajını öyle bir şekilde değiştirdiği saldırılardır ki
yönlendirici Y, oluşturma mesajı oraya ulaştığında değişikliği tespit edebilir.
Amacı, Y yönlendiricisine ulaşmadan X ve Y arasında bir yerde bir yönlendirici tarafından değiştirilen mesajın atılmasıdır.
Değişikliğin Y yönlendiricisine ulaşmadan önce atılmadığı durumlarda, tünel oluşturucu yanıttaki bozulmayı tespit etmeli
ve tüneli atmalıdır.

Muhtemel saldırılar:

- Bir oluşturma kaydını değiştirme
- Bir oluşturma kaydını değiştirme
- Bir oluşturma kaydı ekleme veya kaldırma
- Oluşturma kayıtlarının sırasını değiştirme

TODO: Mevcut tasarım tüm bu saldırıları önlüyor mu?

## Tasarım

### Noise Protokol Çerçevesi

Bu öneri, Noise Protokol Çerçevesi [NOISE](https://noiseprotocol.org/noise.html) (Revizyon 34, 2018-07-11) üzerine gereksinimleri sağlamaktadır.
Noise dilinde, Alice başlatıcıdır ve Bob cevaplayıcıdır.

Bu öneri, Noise protokolü Noise_N_25519_ChaChaPoly_SHA256 üzerine kuruludur.
Bu Noise protokolü aşağıdaki ikincilleri kullanır:

- Tek Yönlü El Sıkışma Şeması: N
  Alice kendi statik anahtarını Bob'a iletmez (N)

- DH Fonksiyonu: X25519
  [RFC-7748](https://tools.ietf.org/html/rfc7748)'de belirtildiği gibi 32 bayt uzunluğunda bir anahtarla X25519 DH.

- Şifre Fonksiyonu: ChaChaPoly
  AEAD_CHACHA20_POLY1305 [RFC-7539](https://tools.ietf.org/html/rfc7539) bölüm 2.8'de belirtildiği gibi.
  İlk 4 baytı sıfıra ayarlanmış 12 baytlık nonce.
  [NTCP2](/en/docs/spec/ntcp2/) içinde olanla aynı.

- Karmalama Fonksiyonu: SHA256
  I2P'de yaygın olarak kullanılan standart 32 baytlık karma.


Çerçeveye Eklemeler
``````````````````````````

Hiçbiri.


### El Sıkışma Şemaları

El sıkışmalarında [Noise](https://noiseprotocol.org/noise.html) el sıkışma şemaları kullanılır.

Aşağıdaki harf eşlemesi kullanılır:

- e = tek kullanımlık geçici anahtar
- s = statik anahtar
- p = mesaj yükü

Oluşturma isteği, Noise N şeması ile aynıdır.
Bu aynı zamanda [NTCP2](/en/docs/spec/ntcp2/) içinde kullanılan XK şemasındaki ilk (Oturum İsteği) mesajıdır.


  ```dataspec

<- s
  ...
  e es p ->





  ```


### İstek Şifreleme

Oluşturma isteği kayıtları, tünel oluşturucu tarafından oluşturulur ve bireysel hattın üzerinde asimetrik olarak şifrelenir.
Şu anda bu istek kayıtlarının asimetrik şifrelemesi, [Cryptography](/en/docs/spec/cryptography/) içinde tanımlandığı gibi ElGamal'dır ve bir SHA-256 kontrol toplamı içerir. Bu tasarım iletim gizli değil.

Yeni tasarım, iletim gizliliği, bütünlük ve kimlik doğrulama için bir KDF ile birlikte Noise "N" örüntüsünü, ECIES-X25519 geçici-statik DH, ve ChaCha20/Poly1305 AEAD kullanacaktır.
Alice, tünel oluşturma isteği yapan kişidir. Tüneldeki her atlama bir Bob'dur.


(Yük Güvenlik Özellikleri)

  ```text

N:                      Kimlik Doğrulama   Gizlilik
    -> e, es                  0                2

    Kimlik Doğrulama: Yok (0).
    Bu yük, bir aktif saldırgan dahil herhangi bir taraf tarafından gönderilmiş olabilir.

    Gizlilik: 2.
    Bilinen bir alıcıya şifreleme, sadece gönderenin ifşası için iletim gizliliği, yeniden oynatmaya karşı savunmasız.
    Bu yük, yalnızca alıcının statik anahtar çiftini içeren DH'lere dayalı olarak şifrelenmiştir.
    Alıcının statik özel anahtarı, hatta daha sonra ifşa edilse bile, bu yük deşifre edilebilir.
    Bu mesajın ayrıca yeniden oynatılma olasılığı vardır, çünkü alıcıdan gelen bir geçici katkı yoktur.

    "e": Alice yeni bir geçici anahtar çifti üretir ve bunu e
         değişkeninde saklar, geçici ortak anahtarı açık metin olarak
         mesaj tamponuna yazar ve eski h ile birlikte
         yeni bir h türetmek üzere karmalar.

    "es": Alice'in geçici anahtar çifti ile
          Bob'un statik anahtar çifti arasında bir DH gerçekleştirilir.
          Sonuç, eski ck ile birlikte karmalanır
          yeni bir ck ve k türetmek için, ve n sıfıra ayarlanır.




  ```



### Yanıt Şifreleme

Oluşturma yanıt kayıtları, atlama oluşturucu tarafından oluşturulur ve oluşturucuya simetrik olarak şifrelenir.
Bu simetrik yanıt kayıtlarının şifrelemesi şu anda bir SHA-256 kontrol toplamı ile birlikte AES'tir.
Bu tasarım iletim gizli değil.

Yeni tasarım, bütünlük ve kimlik doğrulama için ChaCha20/Poly1305 AEAD kullanacaktır.


### Gerekçe

İstek içindeki geçici ortak anahtar AES veya Elligator2 ile gizlenmeye gerek yoktur.
Önceki atlama bunu görebilen tek kişidir ve o atlama
bir sonraki atlamanın ECIES olduğunu bilir.

Yanıt kayıtları, başka bir DH ile tam asimetrik şifreleme gerektirmez.



## Spesifikasyon



### Oluşturma İstek Kayıtları

Şifrelenmiş BuildRequestRecords, hem ElGamal hem de ECIES için uyumluluk amacıyla 528 bayttır.


İstek Kaydı Şifrelenmemiş (ElGamal)
`````````````````````````````````````````

Referans için, bu [I2NP](/en/docs/spec/i2np/) alınmış ElGamal yönlendiriciler için tünel BuildRequestRecord'un mevcut spesifikasyonudur.
Şifrelenmeden önce veriyle birlikte şifreli olmayan bir bayt ve verinin SHA-256 karması eklenir, [Cryptography](/en/docs/spec/cryptography/) içinde tanımlandığı gibi.

Tüm alanlar büyük endian formatındadır.

Şifrelenmemiş boyut: 222 bayt

  ```dataspec


bytes     0-3: mesajları almak için gerekli tünel ID'si, sıfır olmayan
  bytes    4-35: yerel yönlendirici kimlik karması
  bytes   36-39: bir sonraki tünel ID'si, sıfır olmayan
  bytes   40-71: bir sonraki yönlendirici kimlik karması
  bytes  72-103: AES-256 tünel katman anahtarı
  bytes 104-135: AES-256 tünel IV anahtarı
  bytes 136-167: AES-256 yanıt anahtarı
  bytes 168-183: AES-256 yanıt IV
  byte      184: bayraklar
  bytes 185-188: istek zamanı (epocha saat cinsinden, aşağı yuvarlanmış)
  bytes 189-192: bir sonraki mesaj ID'si
  bytes 193-221: yorumlanmamış / rastgele dolgu




  ```


İstek Kaydı Şifrelenmiş (ElGamal)
`````````````````````````````````````

Referans için, bu [I2NP](/en/docs/spec/i2np/) alınmış ElGamal yönlendiriciler için tünel BuildRequestRecord'un mevcut spesifikasyonudur.

Şifrelenmiş boyut: 528 bayt

  ```dataspec


bytes    0-15: Atlama kesilmiş kimlik karması
  bytes  16-528: ElGamal şifrelenmiş BuildRequestRecord




  ```




İstek Kaydı Şifrelenmemiş (ECIES)
```````````````````````````````````````

Bu, ECIES-X25519 yönlendiriciler için tünel BuildRequestRecord'un önerilen spesifikasyonudur.
Değişikliklerin özeti:

- Kullanılmayan 32 baytlık yönlendirici karması kaldırıldı
- İstek zamanı saatten dakikaya değiştirildi
- Gelecekteki değişken tünel süreleri için bitiş alanı eklendi
- Bayraklar için daha fazla alan eklendi
- Ek oluşturma seçenekleri için Haritalama eklendi
- AES-256 yanıt anahtarı ve IV, atlamanın kendi yanıt kaydı için kullanılmaz
- Şifrelenmemiş kayıt daha uzundur çünkü daha az şifreleme ek yükü vardır


İstek kaydı, herhangi bir ChaCha yanıt anahtarı içermez.
Bu anahtarlar bir KDF'den türetilir. Aşağıya bakın.

Tüm alanlar büyük endian formatındadır.

Şifrelenmemiş boyut: 464 bayt

  ```dataspec


bytes     0-3: mesajları almak için gerekli tünel ID'si, sıfır olmayan
  bytes     4-7: bir sonraki tünel ID'si, sıfır olmayan
  bytes    8-39: bir sonraki yönlendirici kimlik karması
  bytes   40-71: AES-256 tünel katman anahtarı
  bytes  72-103: AES-256 tünel IV anahtarı
  bytes 104-135: AES-256 yanıt anahtarı
  bytes 136-151: AES-256 yanıt IV
  byte      152: bayraklar
  bytes 153-155: daha fazla bayrak, kullanılmıyor, uyumluluk için 0'a ayarla
  bytes 156-159: istek zamanı (epoch'dan itibaren dakika cinsinden, aşağı yuvarlanmış)
  bytes 160-163: istek bitiş (oluşturulma zamanından itibaren saniye cinsinden)
  bytes 164-167: bir sonraki mesaj ID'si
  bytes   168-x: tünel oluşturma seçenekleri (Haritalama)
  bytes     x-x: bayraklar veya seçenekler tarafından getirilen başka veriler
  bytes   x-463: rastgele dolgu




  ```

Bayraklar alanı [Tunnel-Creation](/en/docs/spec/tunnel-creation/) içinde tanımlandığı gibi olup, aşağıdaki içeriğe sahiptir::

 Bit sırası: 76543210 (bit 7 MSB'dir)
 bit 7: ayarlıysa, herkesten mesaj alımına izin ver
 bit 6: ayarlıysa, herkese mesaj gönderimine izin ver ve
        yanıtı bir sonraki yüke gönderimuth of the
        belirtilmiş ikinci hop'a bir Tünel Oluşturma Yanıt Mesajıyla gönder
 bitler 5-0: Tanımsız, ilerideki seçeneklerle uyumluluk için 0'a ayarlayın

Bit 7, atlamanın bir giriş ağ geçidi (IBGW) olacağını belirler. Bit 6
atlamanın bir çıkış noktası (OBEP) olacağını belirler. Her iki bit de
birlikte ayarlanamaz.

İstek bitişi gelecekte değişken tünel süreleri için geçerlidir.
Şimdilik, desteklenen tek değer 600'dür (10 dakika).

Tünel oluşturma seçenekleri, [Common](/en/docs/spec/common-structures/) içinde tanımlandığı gibi bir Haritalama yapısıdır.
Bu, gelecekteki kullanım içindir. Şu anda tanımlı herhangi bir seçenek yoktur.
Haritalama yapısı boşsa, bu iki bayttır 0x00 0x00.
Haritalama uzunluğunun (uzunluk alanı dahil) maksimum boyutu 296 bayt,
ve Haritalama uzunluk alanının maksimum değeri 294'tür.



İstek Kaydı Şifrelenmiş (ECIES)
`````````````````````````````````````

Tüm alanlar büyük endian, geçici ortak anahtar ise küçük endian formatındadır.

Şifrelenmiş boyut: 528 bayt

  ```dataspec


bytes    0-15: Atlama kesilmiş kimlik karması
  bytes   16-47: Gönderici geçici X25519 ortak anahtarı
  bytes  48-511: ChaCha20 şifrelenmiş BuildRequestRecord
  bytes 512-527: Poly1305 MAC




  ```



### Oluşturma Yanıt Kayıtları

Şifrelenmiş BuildReplyRecords, hem ElGamal hem de ECIES için uyumluluk amacıyla 528 bayttır.


Yanıt Kaydı Şifrelenmemiş (ElGamal)
`````````````````````````````````````
ElGamal yanıtları AES ile şifrelenir.

Tüm alanlar büyük endian formatındadır.

Şifrelenmemiş boyut: 528 bayt

  ```dataspec


bytes   0-31: Bayt 32-527'nin SHA-256 Karması
  bytes 32-526: rastgele veri
  byte     527: yanıt

  toplam uzunluk: 528




  ```


Yanıt Kaydı Şifrelenmemiş (ECIES)
`````````````````````````````````````
Bu, ECIES-X25519 yönlendiriciler için tünel BuildReplyRecord'un önerilen spesifikasyonudur.
Değişikliklerin özeti:

- Oluşturma yanıt seçenekleri için Haritalama eklendi
- Şifrelenmemiş kayıt daha uzundur çünkü daha az şifreleme ek yükü vardır

ECIES yanıtları ChaCha20/Poly1305 ile şifrelenir.

Tüm alanlar büyük endian formatındadır.

Şifrelenmemiş boyut: 512 bayt

  ```dataspec


bytes    0-x: Tünel Oluşturma Yanıt Seçenekleri (Haritalama)
  bytes    x-x: seçenekler tarafından getirilen başka veriler
  bytes  x-510: Rastgele dolgu
  byte     511: Yanıt baytı




  ```

Tünel oluşturma yanıt seçenekleri, [Common](/en/docs/spec/common-structures/) içinde tanımlandığı gibi bir Haritalama yapısıdır.
Bu, gelecekteki kullanım içindir. Şu anda tanımlı herhangi bir seçenek yoktur.
Haritalama yapısı boşsa, bu iki bayttır 0x00 0x00.
Haritalamanın (uzunluk alanı dahil) maksimum boyutu 511 bayt,
ve Haritalama uzunluk alanının maksimum değeri 509'dur.

Yanıt baytı, parmak izi alınmamak için [Tunnel-Creation](/en/docs/spec/tunnel-creation/) içinde tanımlanan şu değerlerden biridir:

- 0x00 (kabul)
- 30 (TUNNEL_REJECT_BANDWIDTH)


Yanıt Kaydı Şifrelenmiş (ECIES)
```````````````````````````````````

Şifrelenmiş boyut: 528 bayt

  ```dataspec


bytes   0-511: ChaCha20 şifrelenmiş BuildReplyRecord
  bytes 512-527: Poly1305 MAC




  ```

Tam geçişten sonra ECIES kaydı, aralık dolgulama kuralları istek kayıtlarına aynı şekilde uygulanır.


### Kayıtların Simetrik Şifrelenmesi

Karışık tünellere izin verilir ve ElGamal'dan ECIES'e geçiş için gereklidir.
Geçiş dönemi sırasında, giderek artan sayıda yönlendirici ECIES anahtarları altında anahtarlanacaktır.

Simetrik kriptografi ön işlemesi aynı şekilde çalışacaktır:

- "şifreleme":

  - şifre, çözme modunda çalıştırılır
  - istek kayıtları, ön işlemde önden şifre çözülür (şifrelenmiş istek kayıtlarını gizleme)

- "şifre çözme":

  - şifre, şifreleme modunda çalıştırılır
  - istek kayıtları, şifre çözme katılımcı atlamalar tarafından şifrelenir (bir sonraki düz metin istek kaydını açığa çıkarma)

- ChaCha20'nun "modları" yoktur, bu yüzden üç kez çalıştırılır:

  - bir kez ön işlemde
  - bir kez atlama tarafından
  - bir kez son yanıt işlemekte

Karışık tüneller kullanıldığında, tünel oluşturucuları istek kaydının simetrik şifrelemesini
geçerli ve önceki atlamanın şifreleme türüne dayandırmalıdır.

Her atlama, kendi şifreleme türünü kullanarak BuildReplyRecords'u ve Değişken Tünel Oluşturma Mesajı'nı (VTBM) şifreleyecektir.

Yanıt yolunda, uç nokta (gönderen), [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption) kullanarak her atlamanın yanıt anahtarı kullanılarak şifreleme işlemine son verecektir.

Açıklayıcı bir örnek olarak, ElGamal ile çevrili bir ECIES ile bir çıkış tüneline bakalım:

- Gönderen (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tüm BuildRequestRecords şifrelenmiş durumdadır (ElGamal veya ECIES kullanılarak).

AES256/CBC şifresi, kullanıldığında, her kayıt için hala kullanılır, birden çok kayıt boyunca zincirleme olmadan.

Aynı şekilde, ChaCha20, her kaydı şifrelemek için kullanılacaktır, tüm VTBM boyunca yayınlanmadan.

İstek kayıtları Gönderen (OBGW) tarafından ön işlemden geçirilir:

- H3'ün kaydı, aşağıdakiler kullanılarak "şifrelenir":

  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

- H2'nin kaydı, aşağıdakiler kullanılarak "şifrelenir":

  - H1'in yanıt anahtarı (AES256/CBC)

- H1'in kaydı simetrik şifreleme olmadan çıkar

Yalnızca H2 yanıt şifreleme bayrağını kontrol eder ve kendisinden sonra AES256/CBC olduğunu görür.

Her atlama tarafından işlendiğinde, kayıtlar "şifrelenmemiş" bir durumda olacaktır:

- H3'ün kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)

- H2'nin kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)

- H1'in kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)

Tünel yaratıcı, yani İç Uç Nokta (IBEP), yanıtı aşağıdaki gibi işler:

- H3'ün kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)

- H2'nin kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20-Poly1305)

- H1'in kaydı, aşağıdakiler kullanılarak "şifrelenmiştir":

  - H3'ün yanıt anahtarı (AES256/CBC)
  - H2'nin yanıt anahtarı (ChaCha20)
  - H1'in yanıt anahtarı (AES256/CBC)


### İstek Kayıt Anahtarları (ECIES)

Bu anahtarlar, ElGamal BuildRequestRecord'larda açıkça yer alır.
ECIES BuildRequestRecords için, tünel anahtarları ve AES yanıt anahtarları yer alır, ancak ChaCha yanıt anahtarları DH değişiminden türetilir.
Yönlendirici statik ECIES anahtarları için ayrıntılar ve detaylar için [Prop156](/en/proposals/156-ecies-routers/) adresine bakınız.

Aşağıda, daha önce istek kayıtlarında iletilen anahtarların nasıl türetileceğine ilişkin bir açıklama bulunmaktadır.


İlk ck ve h için KDF
````````````````````````

Bu, "N" örüntülü standart [NOISE](https://noiseprotocol.org/noise.html) ve standart bir protokol adıdır.

  ```text

Bu e mesaj örüntüsüdür:

  // protokol_adını tanımlayın.
  protokol_adını ayarlayın = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bayt, US-ASCII kodlu, NULL sonlandırmasız).

  // Hash h = 32 bayt tanımlayın
  // 32 bayta sıfırlayın. 32 bayttan fazla olmadığından hash'lemeyin.
  h = protokol_adı || 0

  32 bayt zincir anahtarı tanımlayın. h verilerini ck'ye kopyalayın.
  zincirAnahtarı olarak ayarlayın = h

  // MixHash(null prologue)
  h = SHA256(h);

  // Buraya kadar, tüm yönlendiriciler tarafından önceden hesaplanabilir.




  ```


İstek Kaydı için KDF
````````````````````````

ElGamal tünel oluşturucuları, tünelin her bir ECIES hattı için bir geçici X25519 anahtar çifti üretir ve yukarıdaki
şema kullanılarak BuildRequestRecord'larını şifreler.
ElGamal tünel oluşturucuları, ElGamal atlamalarına şifreleme yaparken bu standart öncesi şemayı kullanacaklardır.

ECIES tünel oluşturucuları, ElGamal hattının genel anahtarına şifreleme yaparken
[Tunnel-Creation](/en/docs/spec/tunnel-creation/) içinde tanımlanan standart kullanacaklardır. ECIES tünel oluşturucuları,
ECIES atlamalarına şifreleme yaparken yukarıdaki şemayı kullanacaklardır.

Bu, tünel atlamalarının şifreleme türünden yalnızca kendi türlerine ait olan şifrelenmiş kayıtlarını görecekleri anlamına gelir.

ElGamal ve ECIES tünel oluşturucuları için, ECIES atlamalarına şifreleme yaparken benzersiz geçici X25519 anahtar çiftleri
üreteceklerdir.

**ÖNEMLİ**:
Geçici anahtarlar her ECIES atlaması ve her kayıt oluşturma için benzersiz olmalıdır.
Benzersiz anahtarlar kullanılmaması, işbirlikçi atlamaların aynı tünelde olduklarını doğrulamak
için bir saldırı vektörünü açar.


  ```dataspec


// Her atlamanın yönlendirici kimliğinden alınan X25519 statik anahtar çifti (hesk, hepk)
  hesk = ÖZEL_ÜRETİM()
  hepk = HALK_TÜRET(hesk)

  // MixHash(hepk)
  // || aşağıda ekle anlamına gelir
  h = SHA256(h || hepk);

  // Buraya kadar, her yönlendirici tarafından
  // tüm gelen oluşturma talepleri için önceden hesaplanabilir

  // Gönderen, VTBM'deki her bir ECIES atlaması için bir X25519 geçici anahtar çifti üretir (sesk, sepk)
  sesk = ÖZEL_ÜRETİM()
  sepk = HALK_TÜRET(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  E mesaj şablonunun sonu.

  Bu es mesaj şablonudur:

  // Noise es
  // Gönderen, Atlama'nın statik genel anahtarı ile bir X25519 DH gerçekleştirir.
  // Her Atlama, kendi kesilmiş kimlik karmasıyla kayıt bulur,
  // ve şifrelenmiş kayıttan önce Gönderen'in geçici anahtarını çıkarır.
  paylaşılanGizliAnahtar = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[zincirAnahtarı, k] = MixKey(paylaşılanGizliAnahtar)
  // Şifre çözücünün/deşifreleyicinin ChaChaPoly parametreleri
  anahtarVeri = HKDF(zincirAnahtarı, paylaşılanGizliAnahtar, "", 64)
  // Yanıt Kaydı KDF sakla
  zincirAnahtarı = anahtarVeri[0:31]

  // AEAD parametreleri
  k = anahtarVeri[32:63]
  n = 0
  düz metin = 464 bayt oluşturma istek kaydı
  ek olarak h
  şifrelenmiş metin = ENCRYPT(k, n, düz metin, ek)

  Es mesaj şablonunun sonu.

  // MixHash(şifreli metin)
  // Yanıt Kaydı KDF için sakla
  h = SHA256(h || şifreli metin)





  ```

``yanıtAnahtarı``, ``katmanAnahtarı`` ve ``katmanIV`` hala ElGamal kayıtlarına dahil edilmelidir,
ve rastgele olarak üretilebilir.


### İstek Kaydı Şifreleme (ElGamal)

[Tunnel-Creation](/en/docs/spec/tunnel-creation/) içinde tanımlandığı gibi.
ElGamal atlamalarına şifreleme için herhangi bir değişiklik yoktur.




### Yanıt Kaydı Şifreleme (ECIES)

Yanıt kaydı ChaCha20/Poly1305 ile şifrelenmiştir.

  ```dataspec


// AEAD parametreleri
  k = oluşturma isteğinden gelen zincir anahtarı
  n = 0
  düz metin = 512 bayt oluşturma yanıt kaydı
  ek olarak oluşturma isteğinden gelen h

  şifreli metin = ENCRYPT(k, n, düz metin, ek)




  ```



### Yanıt Kaydı Şifreleme (ElGamal)

[Tunnel-Creation](/en/docs/spec/tunnel-creation/) içinde tanımlandığı gibi.
ElGamal atlamalarına şifreleme için herhangi bir değişiklik yoktur.



### Güvenlik Analizi

ElGamal Tünel Oluşturma Mesajları için iletim gizliliği sağlamaz.

AES256/CBC, yalnızca bilinen bir açık metin 'düğüm' saldırısından teorik bir zayıflatmaya karşı savunmasız kalır.

AES256/CBC'ye karşı bilinen pratik saldırı, IV'nin saldırgan tarafından bilindiği bir yastık oracle saldırısıdır.

Bir saldırgan, bir sonraki atlamanın ElGamal şifresini kırarak, AES256/CBC anahtar bilgilerini (yanıt anahtarı ve IV) elde etmelidir.

ElGamal, ECIES'e göre çok daha fazla CPU gücü gerektirir ve bu da potansiyel kaynak tükenmesine işaret eder.

ECIES, her Geçici Kayıt veya Değişken Tünel Oluşturma Mesajı için yeni geçici anahtarlar kullanıldığında iletim gizliliği sağlar.

ChaCha20Poly1305, alıcının mesaj bütünlüğünü şifre çözme işlemine başlamadan önce doğrulamasına izin veren AEAD şifrelemesi sağlar.


## Gerekçe

Bu tasarım mevcut kriptografik ikincillerin, protokollerin ve kodların yeniden kullanımını en üst düzeye çıkarır.
Bu tasarım, riski en aza indirir.




## Uygulama Notları

* Daha eski yönlendiriciler, atlamanın şifreleme türünü kontrol etmez ve ElGamal şifrelenmiş kayıtlar gönderir. Bazı son yönlendiriciler hatalıdır ve çeşitli türlerde hatalı kayıtlar gönderir.
  Uygulayıcılar mümkünse, bunları daha önce DH işleminden önce reddetmelidir
  CPU kullanımını azaltmak için.


## Sorunlar



## Geçiş

Bkz. [Prop156](/en/proposals/156-ecies-routers/).



