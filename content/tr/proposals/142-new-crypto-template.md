---
title: "Yeni Şifreleme Öneri Şablonu"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Genel Bakış

Bu belge, ElGamal asimetrik şifrelememizin yerine yenisini önerirken veya ekleme yaparken dikkate alınması gereken önemli konuları tanımlar.

Bu, bilgilendirici bir belgedir.


## Motivasyon

ElGamal eski ve yavaştır, ve daha iyi alternatifler mevcuttur.
Ancak, herhangi bir yeni algoritmayı ekleyebilmemiz veya değiştirebilmemiz için çözülmesi gereken birkaç mesele bulunmaktadır.
Bu belge, bu çözülmemiş meseleleri vurgulamaktadır.


## Arka Plan Araştırması

Yeni kripto öneren birisi, öncelikle aşağıdaki belgeleri tanımalıdır:

- [Öneri 111 NTCP2](/tr/proposals/111-ntcp-2/)
- [Öneri 123 LS2](/tr/proposals/123-new-netdb-entries/)
- [Öneri 136 deneysel imza türleri](/tr/proposals/136-experimental-sigtypes/)
- [Öneri 137 isteğe bağlı imza türleri](/tr/proposals/137-optional-sigtypes/)
- Yukarıdaki her bir öneri için buradaki tartışma başlıkları, bağlantılar içinde
- [2018 öneri öncelikleri](http://zzz.i2p/topics/2494)
- [ECIES önerisi](http://zzz.i2p/topics/2418)
- [yeni asimetrik kripto genel bakış](http://zzz.i2p/topics/1768)
- [Düşük seviyeli kripto genel bakış](/tr/docs/specs/common-structures/)


## Asimetrik Kripto Kullanımları

Bir inceleme olarak, ElGamal'ı şu amaçlarla kullanıyoruz:

1) Tünel Kurma mesajları (anahtar RouterIdentity'de)

2) Netdb ve diğer I2NP mesajlarının yönlendiriciye-yönlendirici şifrelemesi (Anahtar RouterIdentity'de)

3) İstemci Uçtan-uca ElGamal+AES/OturumEtiketi (anahtar LeaseSet'de, Hedef anahtar kullanılmaz)

4) Geçici DH için NTCP ve SSU


## Tasarım

ElGamal'ı başka bir şeyle değiştirme önerisi, aşağıdaki ayrıntıları sağlamalıdır.


## Şartname

Yeni asimetrik kripto için herhangi bir öneri, aşağıdaki şeyleri tam olarak belirtmelidir.


### 1. Genel

Önerinizde aşağıdaki soruları yanıtlayın. Bunun, aşağıdaki 2)'deki detaylardan ayrı bir öneri olması gerekebileceğini unutmayın, çünkü mevcut öneriler 111, 123, 136, 137 veya diğerleri ile çelişebilir.

- Yukarıdaki 1-4 durumlarının hangisi için yeni kriptoyu kullanmayı öneriyorsunuz?
- 1) veya 2) (yönlendirici) için ise, genel anahtar nereye gidiyor, RouterIdentity'de mi yoksa RouterInfo özelliklerinde mi? Anahtar sertifikası içinde kripto türünü kullanmayı düşünüyor musunuz? Tamamen belirtin. Kararınızı her iki şekilde de gerekçelendirin.
- 3) (istemci) için ise, genel anahtarı hedefte saklamayı ve ECIES önerisinde olduğu gibi anahtar sertifikası içindeki kripto türünü kullanmayı mı, yoksa öneri 123'te olduğu gibi LS2 içinde mi saklamayı mı, yoksa başka bir şeyi mi düşünüyorsunuz? Tamamen belirtin ve kararınızı gerekçelendirin.
- Tüm kullanım alanları için, destek nasıl duyurulacak? 3) içinse, LS2 içinde mi yoksa başka bir yerde mi gitmesi gerekiyor? 1) ve 2) içinse, öneri 136 ve/veya 137'ye benzer mi? Tamamen belirtin ve kararlarınızı gerekçelendirin. Bunun için muhtemelen ayrı bir öneriye ihtiyaç duyulacak.
- Bunun nasıl ve neden geriye dönük uyumlu olduğunu tamamen belirtin, ve bir geçiş planını tamamen belirtin.
- Hangi uygulanmamış öneriler, öneriniz için ön koşuldur?


### 2. Belirli kripto türü

Önerinizde aşağıdaki soruları yanıtlayın:

- Genel kripto bilgisi, belirli eğriler/parametreler, seçiminizi tamamen gerekçelendirin. Teklif ve diğer bilgilerin bağlantılarını sağlayın.
- Etki hız testi sonuçları, ElG ve diğer alternatiflerle karşılaştırıldığında uygulanabilir. Şifreleme, şifre çözme ve anahtar üretimi dahil.
- C++ ve Java'da (hem OpenJDK, BouncyCastle, hem de 3. taraf) kütüphane kullanılabilirliği.
  3. taraf veya Java dışı kütüphaneler için bağlantılar ve lisanslar sağlayın
- Önerilen kripto türü numarası (deneysel aralık veya değil)


## Notlar


